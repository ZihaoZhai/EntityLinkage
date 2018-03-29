import sys
import os
import json
import copy
import matplotlib.pyplot as plt
packagePath='rltk'
sys.path.append(packagePath)
import rltk
from sklearn.cluster import SpectralClustering
tk = rltk.init()
reload(sys) 
sys.setdefaultencoding('utf8')

def readGroundTruth(groundTruthPath):
	groundTruthPairSet={'PER':set(),'LOC':set(),'GPE':set(),'ORG':set()}
	groundTruthFiles=os.listdir(groundTruthPath)
	for f in groundTruthFiles:
		input=open(groundTruthPath+'/'+f,'r')
		data=json.loads(input.read())
		for i in xrange(len(data['originalNames'])):
			for j in xrange(i+1,len(data['originalNames'])):
				groundTruthPairSet[data['type']].add((data['originalNames'][i]['name'],data['originalNames'][j]['name']))
	return groundTruthPairSet

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

def pickTopicWords(wordsList,thr,stringSimilarity):
	topicWords={"PER":[],"LOC":[],"GPE":[],"ORG":[]}
	for tp in wordsList:
		for d in wordsList[tp]:
			#print tp,d
			haveName=0
			mostSimilar=[-1,None]
			for ele in topicWords[tp]:
				for n in ele['originalNames']:
					if n['name']==d[0]:
						n['docIds'].append(d[1])
						haveName=1
						break
					else:
						if stringSimilarity=='trigram_jaccard_similarity':
							similarity=n_char_token_jaccard_similarity(n['name'].lower(),d[0].lower(),3)
						elif stringSimilarity=='jaccard_index_similarity':
							similarity=tk.jaccard_index_similarity(set(n['name'].lower().split(' ')), set(d[0].lower().split(' ')))
						elif stringSimilarity=='jaro_winkler_similarity':
							similarity=tk.jaro_winkler_similarity(n['name'].lower(), d[0].lower(), threshold=0.7, scaling_factor=0.1, prefix_len=4)
						elif stringSimilarity=='levenshtein_similarity':
							similarity=tk.levenshtein_similarity(n['name'].encode().lower(), d[0].encode().lower())
						elif stringSimilarity=='monge_elkan_similarity':
							similarity=tk.monge_elkan_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
						elif stringSimilarity=='needleman_wunsch_similarity':
							similarity=tk.needleman_wunsch_similarity(n['name'].lower(),d[0].lower())
						elif stringSimilarity=='string_cosine_similarity':
							similarity=tk.string_cosine_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
						elif stringSimilarity=='symmetric_monge_elkan_similarity':
							similarity=tk.symmetric_monge_elkan_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
						if similarity>mostSimilar[0] and similarity>=thr:
							mostSimilar[0]=similarity
							mostSimilar[1]=ele
				if haveName==1:
					break
			if haveName==0:
				if mostSimilar[0]!=-1:
					obj={
							'name':d[0],
							'docIds':[d[1]]
						}
					mostSimilar[1]['originalNames'].append(obj)
					#if len(d[0])>len(mostSimilar[1]['preferredName']):
					#	mostSimilar[1]['preferredName']=d[0]
				else:
					obj={
						"preferredName" : d[0],
						"type":tp,
						"originalNames":[
							{
								"name":d[0],
								"docIds":[d[1]]
							}
						]
					}
					topicWords[tp].append(obj)
	for tp in topicWords:
		for i in xrange(len(topicWords[tp])):
			topicWords[tp][i]['originalNames'].sort(key=lambda x:x['name'])
			maxLen=0
			maxName=''
			for on in topicWords[tp][i]['originalNames']:
				if len(on['docIds'])>maxLen:
					maxLen=len(on['docIds'])
					maxName=on['name']
			topicWords[tp][i]['preferredName']=maxName
	return topicWords

def spectralClustering(wordsList,stringSimilarity,groundTruthPath,thr):
	groundTruthFiles=os.listdir(groundTruthPath)
	typeClusterNum={'PER':0,'ORG':0,'LOC':0,'GPE':0}
	for gtf in groundTruthFiles:
		if gtf!='.DS_Store':
			input=open(groundTruthPath+gtf,'r')
			data=input.read()
			data=json.loads(data)
			typeClusterNum[data['type']]+=1
	matrix={'PER':[],'LOC':[],'GPE':[],'ORG':[]}
	clusters={'PER':[],'LOC':[],'GPE':[],'ORG':[]}
	wordsSet={'PER':set([]),'LOC':set([]),'GPE':set([]),'ORG':set([])}
	clusterLabelDic={'PER':{},'LOC':{},'ORG':{},'GPE':{}}
	for tp in wordsList:
		for enti in wordsList[tp]:
			wordsSet[tp].add(enti[0])
		wordsSet[tp]=sorted(list(wordsSet[tp]))
	'''
	tyy='PER'
	for w1 in wordsSet[tyy]:
		row=[]
		for w2 in wordsSet[tyy]:
			similarity=n_char_token_jaccard_similarity(w1.lower(),w2.lower(),3)
			similarity=abs(0) if similarity<thr else similarity
			row.append(similarity)
		matrix[tp].append(row)
	spectral=SpectralClustering(n_clusters=typeClusterNum[tp],affinity="precomputed")
	clusterLabels=spectral.fit_predict(matrix[tp])
	print len(clusterLabels)
	'''
	for tp in wordsSet:
		num=0
		for w1 in wordsSet[tp]:
			row=[]
			for w2 in wordsSet[tp]:
				if stringSimilarity=='trigram_jaccard_similarity':
					similarity=n_char_token_jaccard_similarity(w1.lower(),w2.lower(),3)
				elif stringSimilarity=='jaccard_index_similarity':
					similarity=tk.jaccard_index_similarity(set(w1.lower().split(' ')), set(w2.lower().split(' ')))
				elif stringSimilarity=='jaro_winkler_similarity':
					similarity=tk.jaro_winkler_similarity(w1.lower(), w2.lower(), threshold=0.7, scaling_factor=0.1, prefix_len=4)
				elif stringSimilarity=='levenshtein_similarity':
					similarity=tk.levenshtein_similarity(w1.encode().lower(), w2.encode().lower())
				elif stringSimilarity=='monge_elkan_similarity':
					similarity=tk.monge_elkan_similarity(w1.lower().split(' '),w2.lower().split(' '))
				elif stringSimilarity=='needleman_wunsch_similarity':
					if w1==w2:
						similarity=1
					else:
						similarity=tk.needleman_wunsch_similarity(w1.lower(),w2.lower())
				elif stringSimilarity=='string_cosine_similarity':
					similarity=tk.string_cosine_similarity(w1.lower().split(' '),w2.lower().split(' '))
				elif stringSimilarity=='symmetric_monge_elkan_similarity':
					similarity=tk.symmetric_monge_elkan_similarity(w1.lower().split(' '),w2.lower().split(' '))
				#if similarity<thr:
				#	similarity=0
				similarity=0 if similarity<thr and similarity!=0 else similarity
				row.append(similarity)

			#print num,row
			num+=1
			matrix[tp].append(row)
		#print '\n'
		#print tp,len(matrix[tp])
		#spectral=SpectralClustering(n_clusters=typeClusterNum[tp],affinity="precomputed")
		spectral=SpectralClustering(n_clusters=typeClusterNum[tp],affinity="precomputed",eigen_solver='arpack')
		clusterLabels=spectral.fit_predict(matrix[tp])
		#print len(clusterLabels),len(set(clusterLabels)),max(clusterLabels)
		for i in range(len(clusterLabels)):
			clusterLabelDic[tp][wordsSet[tp][i]]=int(clusterLabels[i])
		for i in xrange(len(set(clusterLabels))):
			obj={
				'preferredName':'',
				'type':tp,
				'originalNames':[]
			}
			clusters[tp].append(obj)
		#print len(clusters[tp])
		#print len(clusterLabels),len(matrix[tp]),len(clusters[tp]),len(clusterLabelDic[tp]),len(wordsSet[tp]),len(wordsList[tp])
		for w in wordsList[tp]:	
			#print clusters[tp][clusterLabelDic[tp][w[0]]]
			if len(w[0])>len(clusters[tp][clusterLabelDic[tp][w[0]]]['preferredName']):
				clusters[tp][clusterLabelDic[tp][w[0]]]['preferredName']=w[0]
			hav=0
			for on in clusters[tp][clusterLabelDic[tp][w[0]]]['originalNames']:
				if on['name']==w[0]:
					on['docIds'].append(w[1])
					hav=1
					break
			if hav==0:
				obj={
					'name':w[0],
					'docIds':[w[1]]
				}
				clusters[tp][clusterLabelDic[tp][w[0]]]['originalNames'].append(obj)
		for tp in clusters:
			for i in xrange(len(clusters[tp])):
				clusters[tp][i]['originalNames'].sort(key=lambda x:x['name'])
	return clusters

def drawGraph(performanceResult):
	plt.subplot2grid((9,9),(0,0),rowspan=4,colspan=8)
	print len(performanceResult["thresholdsList"]),len(performanceResult["fScoreList"]['PER'])
	plt.plot(performanceResult["thresholdsList"], performanceResult["fScoreList"]['PER'], '.-',label='PER')
	plt.plot(performanceResult["thresholdsList"], performanceResult["fScoreList"]['ORG'], '.-',label='ORG')
	plt.plot(performanceResult["thresholdsList"], performanceResult["fScoreList"]['LOC'], '.-',label='LOC')
	plt.plot(performanceResult["thresholdsList"], performanceResult["fScoreList"]['GPE'], '.-',label='GPE')
	plt.axis([0, 1, 0, 1])
	plt.ylabel('F-Score')
	plt.xlabel('Threshold')
	plt.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0)
	plt.grid(True)
	plt.title('Performance Curve')
	plt.subplot2grid((9,9),(5,0),rowspan=4,colspan=8)
	plt.plot(performanceResult["recallList"]['PER'], performanceResult["precisionList"]['PER'], '.-',label='PER')
	plt.plot(performanceResult["recallList"]['ORG'], performanceResult["precisionList"]['ORG'], '.-',label='ORG')
	plt.plot(performanceResult["recallList"]['LOC'], performanceResult["precisionList"]['LOC'], '.-',label='LOC')
	plt.plot(performanceResult["recallList"]['GPE'], performanceResult["precisionList"]['GPE'], '.-',label='GPE')
	plt.axis([0, 1, 0, 1])
	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0)
	plt.grid(True)
	plt.show()
		

	
	






