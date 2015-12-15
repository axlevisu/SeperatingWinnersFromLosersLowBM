import csv
import sys
import statistics as stat
from operator import *
# Transpose of a list
def transpose(alist):
	return map(list, zip(*alist))

# Read and store in 2D Array
datafile = open(sys.argv[1],'r')
# datafile = open("2006d.csv",'r') for example
datareader = csv.reader(datafile, delimiter =",")
data = list(datareader)
# To access values based on names instead of indexes(no hardcoding)
useful_info = [data[1],data[4]]

set_list = list(set(useful_info[0]))
set_list.sort()
set_list_indexing = ['n','a','f','q']
set_list_dict = {set_list[i]:set_list_indexing[i] for i in xrange(4)}
for i in xrange(len(useful_info[1])):
	useful_info[1][i] = set_list_dict[useful_info[0][i]]+useful_info[1][i]
idx= {useful_info[1][i] : [k for k,j in enumerate(useful_info[1]) if j==useful_info[1][i]] for i in xrange(len(useful_info[1]))}
# Delete Unnecessary data
del data[0:5]
#convert to float(to 0 in case of NA and no data)
for i in xrange(0,len(data)):
	for j in xrange(2,len(data[i])):
		try:
			data[i][j] = float(data[i][j])
		except:
			data[i][j] = 0.0
# Calculate F_SCORE
g_score = []
roa =[]
cfo=[]
var_roa=[]
var_gr=[]
rd = []
capex =[]
adv =[]
companies_g4_zero =[]
companies_g5_zero =[]
companies_for_removal =[]
for company in data:
	try:
		var =1
		for i in idx['aAverage total assets']:
			var = var/company[i]
		var = var/company[idx['atotal_assets'][1]]
		q_roa=[]
		q_gr =[]
		ti =[]
		te =[]
		ei =[]
		ee =[]
		ns =[]
		roa.append( (company[idx['aTotal income'][-1]]-company[idx['aTotal expenses'][-1]]-company[idx['aExtra-ordinary income'][-1]]+company[idx['aExtra-ordinary expenses'][-1]])/company[idx['aAverage total assets'][-1]] )
		cfo.append(company[idx['aNet cash flow from operating activities'][-1]]/company[idx['aAverage total assets'][-1]])
		# [list(x) for x in zip(list1, list2)]
		for i in idx['qTotal income']:
			ti.append(company[i])
		for i in idx['qExtra-ordinary expenses']:
			ee.append(company[i])
		for i in idx['qExtra-ordinary income']:
			ei.append(company[i])
		for i in idx['qTotal expenses']:
			te.append(company[i])
		for i in idx['qNet sales']:
			ns.append(company[i])
		for i in xrange(16):
			try:
				q_gr.append((-ns[-20:-4][i]+ns[-16:][i])/ns[-20:-4][i])
			except:
				var=1
		q_roa.append(map(sub,map(add,ti,ee),map(add,te,ei)))
		q_roa = q_roa[0][4:21]
		q_roa[-1] = q_roa[-1]/company[idx['aAverage total assets'][-1]]
		for i in xrange(4):
			for j in xrange(4):
				q_roa[j+4*i] = q_roa[j+4*i]/company[idx['aAverage total assets'][i]]
		q_roa =filter(lambda a: a != 0, q_roa)
		if len(q_roa)<6:
			companies_g4_zero.append(company[0])
			var_roa.append(0)
		else:
			var_roa.append(stat.variance(q_roa))
		if len(q_gr)<6:
			companies_g5_zero.append(company[0])
			var_gr.append(0)
		else:
			var_gr.append(stat.variance(q_gr))
		if company[idx['aNet cash flow from operating activities'][-1]] + company[idx['aTotal expenses'][-1]] > company[idx['aTotal income'][-1]]:
			g_score.append(1)
		else:
			g_score.append(0)
		rd.append(company[idx['aResearch & development expenses'][-1]]/company[idx['atotal_assets'][-1]])
		capex.append((company[idx['aNet fixed assets'][-1]]-company[idx['aIntangible assets, net'][-1]])/company[idx['atotal_assets'][-1]])
		adv.append(company[idx['aAdvertising expenses'][-1]]/company[idx['atotal_assets'][-1]])
	except:
		companies_for_removal.append(company)
for company in companies_for_removal:
	data.remove(company)
data =transpose(data)
data.append(var_gr)
data.append(var_roa)
data.append(roa)
data.append(cfo)
data.append(rd)
data.append(capex)
data.append(adv)
data.append(g_score)
for i in xrange(len(data[idx['nNIC code'][0]])): 
	data[idx['nNIC code'][0]][i] = data[idx['nNIC code'][0]][i][0:3]  
data =transpose(data)
sorted_data = sorted(data,key = lambda x: x[idx['fP/B '][0]])
lowbm_data =  [i for j,i in enumerate(sorted_data) if j not in range(0, len(sorted_data)/2)]
data = lowbm_data
data =transpose(data)
nic_list = list(set(data[idx['nNIC code'][0]]))
data = transpose(data)
indd ={nic_code:[company for company in data if company[idx['nNIC code'][0]]==nic_code] for nic_code in nic_list}
companies_for_removal =[]
keys_to_remove =[]
for i in indd:
	if len(indd[i]) <4:
		companies_for_removal+=indd[i]
		keys_to_remove.append(i)
for company in companies_for_removal:
	data.remove(company)
for key in keys_to_remove:
	del indd[key] 
medians ={}
for i in indd:
	companies = transpose(indd[i]) 
	medians[i]=[]
	for j in xrange(2,7):
		medians[i].append(stat.median(companies[-1*j]))
	medians[i].append(stat.median([company[-7] for company in transpose(companies) if company[0] not in companies_g4_zero]))
	medians[i].append(stat.median([company[-8] for company in transpose(companies) if company[0] not in companies_g5_zero]))
	for company in indd[i]:
		k = data.index(company)
		for j in xrange(2,7):
			data[k][-1]+=1 if data[k][-j]>medians[i][j-2] else 0
		data[k][-1]+=1 if data[k][-7]>medians[i][5] and data[k][0] not in companies_g4_zero else 0
		data[k][-1]+=1 if data[k][-8]>medians[i][6] and data[k][0] not in companies_g5_zero else 0
# gsorted_data = sorted(data, key = lambda x: x[-1])
bottom_decile =[x for x in data if x[-1] in [0,1] ]
top_decile =[x for x in data if x[-1] in [6,7,8] ]
# print transpose(top_decile)[0],transpose(bottom_decile)[0]
with open(sys.argv[2], "a") as myfile:
	myfile.write(sys.argv[1][-9:-5]+"\n"+"long on\n" )
	for company in top_decile:
		myfile.write(company[idx['nCompany Name'][0]] +"  "+str(company[idx['fP/B '][0]])+"  "+str(company[-1]) + "\n")
	myfile.write("\nshort on\n" )
	for company in bottom_decile:
		myfile.write(company[idx['nCompany Name'][0]] +"  "+str(company[idx['fP/B '][0]])+ "  "+str(company[-1])+"\n")
	myfile.write("\n\n" )
returnt = 0
returnb = 0
for company in top_decile:
	returnt+= (company[idx['fAdjusted Closing Price '][0]]-company[idx['fAdjusted Opening Price '][0]])/company[idx['fAdjusted Opening Price '][0]]
returnt = 100*returnt/len(top_decile)
for company in bottom_decile:
	returnb+= (company[idx['fAdjusted Opening Price '][0]]-company[idx['fAdjusted Closing Price '][0]])/company[idx['fAdjusted Opening Price '][0]]
returnb = 100*returnb/len(bottom_decile)
returns = returnt + returnb #+ 7 #bond rate
print returnt, returnb, returns
