import sys
import json
import os
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
packagePath='../rltk'
inputPath=sys.argv[1]
outputPath=sys.argv[2]
if len(sys.argv)==4:
	packagePath=sys.argv[3]
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

files=os.listdir(inputPath)
for f in files:
	if f!='.DS_Store':
		input=open(inputPath+f)
		data=input.read()
		data=json.loads(data)
		pickTopicWords(data,'PER',f)
		pickTopicWords(data,'ORG',f)
		pickTopicWords(data,'GPE',f)
		pickTopicWords(data,'LOC',f)
if not os.path.exists(outputPath):
	os.makedirs(outputPath)
for t in topicWords:
	newData=json.dumps(t)
	ouputFile=outputPath+t['preferredName'].replace('.json','').replace('/','').encode('utf-8')+'_'+t['type'].encode('utf-8')+'.json'
	output=open(ouputFile,'w')
	output.write(newData)
	output.close()