import csv
import sys

# Transpose of a list
def transpose(alist):
	return map(list, zip(*alist))

# Read and store in 2D Array
datafile = open(sys.argv[1],'r')
# datafile = open("2006d.csv",'r') for example
datareader = csv.reader(datafile, delimiter =",")
data = list(datareader)
# To access values based on names instead of indexes(no hardcoding)
useful_info = data[3:5]

for i in xrange(len(useful_info[0])):
	try:
		useful_info[0][i] = int(useful_info[0][i][-2:])
	except:
		useful_info[0][i] = 0

set_list = list(set(useful_info[0]))
set_list.sort()
set_list_indexing = ['n','h','p','c','f']
set_list_dict = {set_list[i]:set_list_indexing[i] for i in xrange(5)}
for i in xrange(len(useful_info[1])):
	useful_info[1][i] = set_list_dict[useful_info[0][i]]+useful_info[1][i]
idx= {useful_info[1][i] : i for i in xrange(len(useful_info[1]))}
# Delete Unnecessary data
del data[0:5]
#convert to float(to 0 in case of NA and no data)
for i in xrange(0,len(data)):
	for j in xrange(1,len(data[i])):
		try:
			data[i][j] = float(data[i][j])
		except:
			data[i][j] = 0.0
# Calculate F_SCORE
f_score = []
# Remove companies without useful data
companies_for_removal =[]
for company in data:
	try:
		score =0
		score+=1 if ( (company[idx['cTotal income']-company[idx['cTotal expenses']]-company[idx['cExtra-ordinary income']]+company[idx['cExtra-ordinary expenses']])/company[idx['pTotal assets']] ) >0 else 0 #ROA
		score+=1 if ( (company[idx['cTotal income']]-company[idx['cTotal expenses']]-company[idx['cExtra-ordinary income']]+company[idx['cExtra-ordinary expenses']])/company[idx['pTotal assets']] ) > ( (company[idx['pTotal income']]-company[idx['pTotal expenses']]-company[idx['pExtra-ordinary income']]+company[idx['pExtra-ordinary expenses']])/company[idx['hTotal assets']] )  else 0 #D_ROA
		score+=1 if ( company[idx['cNet cash flow from operating activities']]/company[idx['pTotal assets']] ) >0 else 0 #CFO
		score+=1 if  ( (company[idx['cTotal income']]-company[idx['cTotal expenses']]-company[idx['cExtra-ordinary income']]+company[idx['cExtra-ordinary expenses']])/company[idx['pTotal assets']] ) < ( company[idx['cNet cash flow from operating activities']]/company[idx['pTotal assets']] )  else 0 #ACCRUAL
		score+=1 if company[idx['cCurrent ratio (times)']] >   company[idx['pCurrent ratio (times)']] else 0 #D_LIQUID
		score+=1 if ( company[idx['cTotal term liabilities']]/company[idx['cAverage total assets']] ) < ( company[idx['pTotal term liabilities']]/company[idx['pAverage total assets']] ) else 0 #D_LEVER
		var = 1/company[idx['cAdjusted Opening Price ']]*company[idx['fAdjusted Closing Price ']]
		try:#D_MARGIN
			score+=1 if ( (company[idx['cNet sales']]-company[idx['cCost of goods sold']])/company[idx['cNet sales']] ) >( (company[idx['pNet sales']]-company[idx['pCost of goods sold']])/company[idx['pNet sales']] ) else 0
		except:
			score+=1 if ( (company[idx['cIncome from financial services']]-company[idx['cCost of goods sold']])/company[idx['cIncome from financial services']] ) >( (company[idx['pIncome from financial services']]-company[idx['pCost of goods sold']])/company[idx['pIncome from financial services']] ) else 0 
		try:#D_TURNOVER
			score+=1 if ( company[idx['cAverage total assets']]/company[idx['cNet sales']] ) <( company[idx['pAverage total assets']]/company[idx['pNet sales']] ) else 0
		except:
			score+=1 if ( company[idx['cAverage total assets']]/company[idx['cIncome from financial services']] ) <( company[idx['pAverage total assets']]/company[idx['pIncome from financial services']] ) else 0
		f_score.append(score)
	except:
		companies_for_removal.append(company)
# print companies_for_removal
for company in companies_for_removal:
	data.remove(company)

data = transpose(data)
data.append(f_score)
data = transpose(data)
# Sorted by BM
bmsorted_data = sorted(data, key = lambda x: x[idx['cP/B ']])
# Take top 50%
highbm_data =[i for j,i in enumerate(bmsorted_data) if j in range(0, len(bmsorted_data)/2)]
# Sorted by f_score
fsorted_data = sorted(highbm_data, key = lambda x: x[-1])
bottom_decile =[i for j,i in enumerate(fsorted_data) if j in range(0, 1+len(fsorted_data)/10)]
top_decile =[i for j,i in enumerate(fsorted_data) if j in range(9*len(fsorted_data)/10, len(fsorted_data))]
# bottom_decile =[x for x in highbm_data if x[-1] in [1,2] ]
# top_decile =[x for x in highbm_data if x[-1] in [7,8] ]
with open(sys.argv[2], "a") as myfile:
	myfile.write(sys.argv[1][-9:-5]+"\n"+"long on\n" )
	for company in top_decile:
		myfile.write(company[idx['nCompany Name']] +"  "+str(company[idx['cP/B ']])+"  "+str(company[-1]) + "\n")
	myfile.write("\nshort on\n" )
	for company in bottom_decile:
		myfile.write(company[idx['nCompany Name']] +"  "+str(company[idx['cP/B ']])+ "  "+str(company[-1])+"\n")
	myfile.write("\n\n" )
	
returnt = 0
returnb = 0
for company in top_decile:
	returnt+= (company[idx['fAdjusted Closing Price ']]-company[idx['cAdjusted Opening Price ']])/company[idx['cAdjusted Opening Price ']]
returnt = returnt/len(top_decile)
for company in bottom_decile:
	returnb+= (company[idx['cAdjusted Opening Price ']]-company[idx['fAdjusted Closing Price ']])/company[idx['cAdjusted Opening Price ']]
returnb = returnb/len(bottom_decile)
returns = returnt + returnb
returns =  (returns*100) #+ 7 #bond rate
print returns
