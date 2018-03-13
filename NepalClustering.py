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
sys.path.append('/Users/zihaozhai/Desktop/Disaster/EntityLinkage/functions')
import rltk
import entityLinkageFunctions
tk = rltk.init()
topicWords=[]
thr=0.8

wordsList={"PER":[],"ORG":[],"GPE":[],"LOC":[]}
files=os.listdir(inputPath)
for f in files:
	if f!='.DS_Store':
		input=open(inputPath+f)
		data=input.read()
		data=json.loads(data)
		for t in wordsList:
			if data.has_key(t):
				for tw in data[t]:
					wordsList[t].append((tw,f))
topicWords=entityLinkageFunctions.pickTopicWordsFromNepal(wordsList,thr)
if not os.path.exists(outputPath):
	os.makedirs(outputPath)
for tp in topicWords:
	for t in topicWords[tp]:
		newData=json.dumps(t)
		ouputFile=outputPath+t['preferredName'].replace('.json','').replace('/','').encode('utf-8')+'_'+t['type'].encode('utf-8')+'.json'
		output=open(ouputFile,'w')
		output.write(newData)
		output.close()






