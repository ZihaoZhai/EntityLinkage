import sys
import json
import os
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
packagePath='../rltk'#modify here
inputPath=sys.argv[1]
outputPath=sys.argv[2]
if len(sys.argv)==4:
	packagePath=sys.argv[3]
sys.path.append(packagePath)
sys.path.append('/Users/zihaozhai/Desktop/LORELEI/EntityLinkage/functions')
import rltk
import entityLinkageFunctions
tk = rltk.init()
topicWords={}
groundTruthPath='../groundTruthOutputJsonData/'
wordsBag={"PER":{},"ORG":{},"GPE":{},"LOC":{}}
ind=0

def pickTopicWordsbyType(wordsBag,thr,stringSimilarity,tp):
	def n_char_token_jaccard_similarity(strA,strB,tokenLen):
		strA='#'*(tokenLen-1)+strA+'#'*(tokenLen-1)
		strB='#'*(tokenLen-1)+strB+'#'*(tokenLen-1)
		if len(strA)<tokenLen:
			setA=set([strA])
		else:
			setA=set()
			for i in xrange(0,len(strA)-tokenLen+1):
				setA.add(strA[i:i+tokenLen])
		if len(strB)<tokenLen:
			setB=set([strB])
		else:
			setB=set()
			for i in xrange(len(strB)-tokenLen+1):
				setB.add(strB[i:i+tokenLen])
		similarity=tk.jaccard_index_similarity(setA, setB)
		return similarity
	topicWords=[]
	for d in wordsBag[tp]:
		haveName=0
		mostSimilar=[-1,None]
		for ele in topicWords:
			for n in ele['originalNames']:
				if n['name']==d:
					n['docIds']+=wordsBag[tp][d]
					haveName=1
					break
				else:
					if stringSimilarity=='trigram_jaccard_similarity':
						similarity=n_char_token_jaccard_similarity(n['name'].lower(),d.lower(),3)
					elif stringSimilarity=='jaccard_index_similarity':
						similarity=tk.jaccard_index_similarity(set(n['name'].lower().split(' ')), set(d.lower().split(' ')))
					elif stringSimilarity=='jaro_winkler_similarity':
						similarity=tk.jaro_winkler_similarity(n['name'].lower(), d.lower(), threshold=0.7, scaling_factor=0.1, prefix_len=4)
					elif stringSimilarity=='levenshtein_similarity':
						similarity=tk.levenshtein_similarity(n['name'].encode().lower(), d.encode().lower())
					elif stringSimilarity=='monge_elkan_similarity':
						similarity=tk.monge_elkan_similarity(n['name'].lower().split(' '),d.lower().split(' '))
					elif stringSimilarity=='needleman_wunsch_similarity':
						similarity=tk.needleman_wunsch_similarity(n['name'].lower(),d.lower())
					elif stringSimilarity=='string_cosine_similarity':
						similarity=tk.string_cosine_similarity(n['name'].lower().split(' '),d.lower().split(' '))
					elif stringSimilarity=='symmetric_monge_elkan_similarity':
						similarity=tk.symmetric_monge_elkan_similarity(n['name'].lower().split(' '),d.lower().split(' '))
					if similarity>mostSimilar[0] and similarity>=thr:
						mostSimilar[0]=similarity
						mostSimilar[1]=ele
			if haveName==1:
				break
		if haveName==0:
			if mostSimilar[0]!=-1:
				obj={
					'name':d,
					'docIds':wordsBag[tp][d]
					}
				mostSimilar[1]['originalNames'].append(obj)
				#if len(d[0])>len(mostSimilar[1]['preferredName']):
				#	mostSimilar[1]['preferredName']=d[0]
			else:
				obj={
					"preferredName" : d,
					"type":tp,
					"originalNames":[
						{
							"name":d,
							"docIds":wordsBag[tp][d]
						}
					]
				}
				topicWords.append(obj)
	for i in xrange(len(topicWords)):
		topicWords[i]['originalNames'].sort(key=lambda x:x['name'])
		maxLen=0
		maxName=''
		for on in topicWords[i]['originalNames']:
			if len(on['docIds'])>maxLen:
				maxLen=len(on['docIds'])
				maxName=on['name']
		topicWords[i]['preferredName']=maxName
	return topicWords

if os.listdir(inputPath)[ind]=='.DS_Store':
	indclear+=1
files=os.listdir(inputPath)
if 'll_nepal_out' in os.listdir(inputPath)[ind]:
	for f in files:
		if f!='.DS_Store':
			input=open(inputPath+f)
			data=input.read()
			data=json.loads(data)
			for t in wordsBag:
				if data.has_key(t):
					for tw in data[t]:
						wordsBag[t][tw]=wordsBag[t].get(tw,[])+[f]
elif 'AWATD' in os.listdir(inputPath)[ind]:
	for f in files:
		if f!='.DS_Store':
			input=open(inputPath+f)
			data=input.read()
			data=json.loads(data)
			for t in wordsBag:
				#if data["_source"].has_key(t):
				if data["_source"].has_key(t) and data["_source"]['topics']!=[]:
					for tw in data["_source"][t]:
						wordsBag[t][tw]=wordsBag[t].get(tw,[])+[f]
for tp in wordsBag:
	if tp=='LOC':
		print tp
		topicWords[tp]=pickTopicWordsbyType(wordsBag,0.3,'trigram_jaccard_similarity',tp)
	elif tp=='ORG':
		print tp
		topicWords[tp]=pickTopicWordsbyType(wordsBag,0.5,'string_cosine_similarity',tp)
	elif tp=='PER':
		print tp
		topicWords[tp]=pickTopicWordsbyType(wordsBag,0.9,'monge_elkan_similarity',tp)
	elif tp=='GPE':
		print tp
		topicWords[tp]=pickTopicWordsbyType(wordsBag,0.85,'symmetric_monge_elkan_similarity',tp)
if not os.path.exists(outputPath):
	os.makedirs(outputPath)
for tp in topicWords:
	print tp,':',len(topicWords[tp])
	for t in topicWords[tp]:
		'''
		if len(t['originalNames'])>1:
			print t['preferredName'],t['type']
			print '-----------------'
			for on in t['originalNames']:
				print on['name'],len(on['docIds'])
			print '\n'
		'''
		newData=json.dumps(t)
		ouputFile=outputPath+t['preferredName'].replace('.json','').replace('/','').encode('utf-8')+'_'+t['type'].encode('utf-8')+'.json'
		output=open(ouputFile,'w')
		output.write(newData)
		output.close()

