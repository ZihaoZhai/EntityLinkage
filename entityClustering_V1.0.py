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
sys.path.append('/Users/zihaozhai/Desktop/LORELEI/EntityLinkage/functions')
import rltk
import entityLinkageFunctions
tk = rltk.init()
topicWords=[]

groundTruthPath='../groundTruthOutputJsonData/'

wordsList={"PER":[],"ORG":[],"GPE":[],"LOC":[]}
#stringSimilarity='trigram_jaccard_similarity'
stringSimilarity='jaccard_index_similarity'
#stringSimilarity='jaro_winkler_similarity'
#stringSimilarity='levenshtein_similarity'
#stringSimilarity='monge_elkan_similarity'
#stringSimilarity='needleman_wunsch_similarity'
#stringSimilarity='string_cosine_similarity'
#stringSimilarity='symmetric_monge_elkan_similarity'
ind=0
if os.listdir(inputPath)[ind]=='.DS_Store':
	ind+=1
files=os.listdir(inputPath)
if 'll_nepal_out' in os.listdir(inputPath)[ind]:
	for f in files:
		if f!='.DS_Store':
			input=open(inputPath+f)
			data=input.read()
			data=json.loads(data)
			for t in wordsList:
				if data.has_key(t):
					for tw in data[t]:
						wordsList[t].append((tw,f))
elif 'AWATD' in os.listdir(inputPath)[ind]:
	for f in files:
		if f!='.DS_Store':
			input=open(inputPath+f)
			data=input.read()
			data=json.loads(data)
			for t in wordsList:
				if data["_source"].has_key(t):
					for tw in data["_source"][t]:
						wordsList[t].append((tw,f))
thr=0.3
topicWords=entityLinkageFunctions.pickTopicWords(wordsList,thr,stringSimilarity)
#thr=0.85
#topicWords=entityLinkageFunctions.spectralClustering(wordsList,stringSimilarity,groundTruthPath,thr)
if not os.path.exists(outputPath):
	os.makedirs(outputPath)
for tp in topicWords:
	for t in topicWords[tp]:
		#if len(t['originalNames'])>1:
		print t['preferredName'],t['type']
		print '-----------------'
		for on in t['originalNames']:
			print on['name'],len(on['docIds'])
		print '\n'
		newData=json.dumps(t)
		ouputFile=outputPath+t['preferredName'].replace('.json','').replace('/','').encode('utf-8')+'_'+t['type'].encode('utf-8')+'.json'
		output=open(ouputFile,'w')
		output.write(newData)
		output.close()


