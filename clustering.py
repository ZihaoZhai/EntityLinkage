import sys
import json
import os
import sys
#import networkx as nx
#G = nx.Graph()
reload(sys) 
sys.setdefaultencoding('utf8')
packagePath='/Users/zihaozhai/Desktop/Trojan/Internship/ISI/rltk'
#inputPath='HitiJsonInput/'
inputPath='ll_nepal/'
outputPath='output/'
#outputPath='HitiJsonOutput/'
sys.path.append(packagePath)
import rltk
tk = rltk.init()
topicWords=[]
thr=0.8
def pickTopicWords(data,tp,file):
	if data.has_key(tp):
		for d in data[tp]:
			haveName=0
			for ele in range(len(topicWords)):
				if topicWords[ele]['type']==tp:
					for n in range(len(topicWords[ele]['originalNames'])):
						if topicWords[ele]['originalNames'][n]['name']==d:
							topicWords[ele]['originalNames'][n]['docIds'].append(file)
							haveName=1
							break
					if haveName==0:
						for n in range(len(topicWords[ele]['originalNames'])):
							similarity=tk.jaccard_index_similarity(set(topicWords[ele]['originalNames'][n]['name'].split(' ')), set(d.split(' ')))
							if similarity>=thr:
								haveName=1
								obj={
									'name':d,
									'docIds':[file]
								}
								topicWords[ele]['originalNames'].append(obj)
								if len(d)>len(topicWords[ele]['preferredName']):
									topicWords[ele]['preferredName']=d						
			if haveName==0:
				obj={
					"preferredName" : d,
					"type":tp,
					"originalNames":[
						{
							"name":d,
							"docIds":[file]
						}
					]
				}
				topicWords.append(obj)
num=1
files=os.listdir(inputPath)
for f in files:
	if num%3000==0:
		print num
	num+=1
	input=open(inputPath+f)
	data=input.read()
	data=json.loads(data)
	pickTopicWords(data,'PER',f)
	pickTopicWords(data,'ORG',f)
	pickTopicWords(data,'GPE',f)
	pickTopicWords(data,'LOC',f)
for t in topicWords:
	'''
	nodeList=[]
	for on in t['originalNames']:
		nodeList+=on['docIds']
	for i in range(len(nodeList)):
		for j in range(i,len(nodeList)):
			G.add_edge(nodeList[i], nodeList[j])
	'''
	newData=json.dumps(t)
	ouputFile=outputPath+t['preferredName'].replace('.json','').replace('/','').encode('utf-8')+'_'+t['type'].encode('utf-8')+'.json'
	output=open(ouputFile,'w')
	output.write(newData)
	output.close()
print G.number_of_nodes(),G.number_of_edges()