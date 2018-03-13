import sys
packagePath='rltk'
sys.path.append(packagePath)
import rltk
tk = rltk.init()
reload(sys) 
sys.setdefaultencoding('utf8')

def threeCharTkenJaccardSimilarity(strA,strB,tokenLen):
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

def pickTopicWordsFromNepal(wordsList,thr):
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
						similarity=threeCharTkenJaccardSimilarity(n['name'].lower(),d[0].lower(),3)
						#similarity=tk.jaccard_index_similarity(set(n['name'].lower().split(' ')), set(d[0].lower().split(' ')))
						#similarity=tk.jaro_winkler_similarity(n['name'].lower(), d[0].lower(), threshold=0.7, scaling_factor=0.1, prefix_len=4)
						#similarity=tk.levenshtein_similarity(n['name'].encode().lower(), d[0].encode().lower())
						#similarity=tk.monge_elkan_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
						#similarity=tk.needleman_wunsch_similarity(n['name'].lower(),d[0].lower())
						#similarity=tk.string_cosine_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
						#similarity=tk.symmetric_monge_elkan_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
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
					if len(d[0])>len(mostSimilar[1]['preferredName']):
						mostSimilar[1]['preferredName']=d[0]
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
	return topicWords

def pickTopicWordsFromHaiti(wordsList,thr):
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
						similarity=threeCharTkenJaccardSimilarity(n['name'].lower(),d[0].lower(),3)
						#similarity=tk.jaccard_index_similarity(set(n['name'].lower().split(' ')), set(d[0].lower().split(' ')))
						#similarity=tk.jaro_winkler_similarity(n['name'].lower(), d[0].lower(), threshold=0.7, scaling_factor=0.1, prefix_len=4)
						#similarity=tk.levenshtein_similarity(n['name'].encode().lower(), d[0].encode().lower())
						#similarity=tk.monge_elkan_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
						#similarity=tk.needleman_wunsch_similarity(n['name'].lower(),d[0].lower())
						#similarity=tk.string_cosine_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
						#similarity=tk.symmetric_monge_elkan_similarity(n['name'].lower().split(' '),d[0].lower().split(' '))
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
					if len(d[0])>len(mostSimilar[1]['preferredName']):
						mostSimilar[1]['preferredName']=d[0]
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
	return topicWords