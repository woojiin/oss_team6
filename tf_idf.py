#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import math
from nltk import word_tokenize
from collections import Counter
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#from tkinter import *
#from tkinter import messagebox
import crawling as cr

es_host = "127.0.0.1"
es_port = "9200"
word_d={}
sent_list=[]
tflist = []
sortedlist = []
cnt  =0
count =0
alldata = {}
swlist = []


def process_new_sentence(s):
	sent_list.append(s)
	tokenized = word_tokenize(s)
	for word in tokenized:
		if word not in word_d.keys():
			word_d[word]=0
		word_d[word] +=1

def compute_tf(s):
	bow = set()
	wordcount_d = {}

	tokenized = word_tokenize(s)
	for tok in tokenized:
		if tok not in wordcount_d.keys():
			wordcount_d[tok]=0
		wordcount_d[tok] +=1
		bow.add(tok)

	tf_d = {}
	for word, cnt in wordcount_d.items():
		tf_d[word]=float(cnt)/len(bow)
	#print(tf_d)

	return tf_d

def compute_idf():
	Dval = len(sent_list)

	bow=set()

	for i in range(0, len(sent_list)):
		tokenized=word_tokenize(sent_list[i])
		for tok in tokenized:
			bow.add(tok)

	idf_d={}
	for t in bow:
		cnt=0
		for s in sent_list:
			if t in word_tokenize(s):
				cnt +=1
			idf_d[t] = float(math.log(float(Dval)/cnt))
			#if cnt ==0:
			#	continue;				
				#print("나누기가 0")
			
			
	#print(idf_d)
	return idf_d

if __name__=='__main__':
	result = []
	url = u'http://abdera.apache.org/'
	es = Elasticsearch([{'host': es_host, 'port':es_port}], timeout= 30)

	tags_body = cr.crawling(url)
	

	#tags_body = soup.find(id="content").get_text().lower()

#	print(tags_body)
	
	
	swlist=[]
	for sw in stopwords.words("english"):
		swlist.append(sw)
	sw_tokenized = word_tokenize(tags_body)

	sw_result=[]
	for w in sw_tokenized:
		if w not in swlist:
			sw_result.append(w)

	str_result=' '.join(sw_result)

	 # 엘라스틱 서치에서 모든 URL을 읽어와서 alldata에 담기
	temp = {}
	query = {"query": {"bool": {"must":[{"match": {"flag": 1}}]}}}
	docs = es.search(index= 'word', body = query, size = 10)
	if docs['hits']['total']['value']>0:	
		for doc in docs['hits']['hits']:
			#크롤링
			cr_data = cr.crawling(doc['_source']['url'])
			#프로세
			process_new_sentence(cr_data)	
			#temp["url"] = doc['_source']['url']
			#temp["words"] = doc['_source']['words']
			#alldata[count] = temp
			#print(alldata[count])
			#count = count + 1


	process_new_sentence(str_result) #여기에 result를 넣어줘야
	idf_d = compute_idf()
	temp = {}
	#sprint(idf_d)
	for i in range(0, len(sent_list)):
		tf_d = compute_tf(sent_list[i])
		#print(tf_d)
		for word, tfval in tf_d.items():	
			print(word, tfval*idf_d[word])
		#print(" ")
			#print(key)
			#print(value)
			
			#tfidf=value*idf_d[key]
			#print(idf_d[key])
			#print(tfidf)
			#print()
			#if key== 'copyright':
			#	break
			#temp["word"] = key
			#temp["tfidf"] = tfidf
			#alldata[count] = temp
			#count = count+1
			
	#print(alldata)
			
		 

	#print(tf_idf)
	#print(len(sent_list))
	
	#d=Counter(tf_idf)
	#print(d)
	#tflist = tf_idf.items()
	#print(tflist)
	#sortedlist = sorted(tflist, key = lambda x: x[1], reverse = True)
	
	#for (k,v) in sortedlist:
	#	if cnt>=10:	
	#		break
	#	print(k)
		#print(v)
		#print()
	#	cnt +=1
		
		
	#for k, v in d.most_common(10):	#가장 많이 나타난 10개
	#	print(k)
		
	#print("    ")
