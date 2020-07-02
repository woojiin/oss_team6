#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import re
import requests
import nltk
import numpy
import crawling
import time
nltk.download('punkt')
nltk.download('stopwords')
from bs4 import BeautifulSoup
from flask import Flask, render_template
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import crawling as cr
es_host = "127.0.0.1"
es_port = "9200"

word_d ={}
sent_list = []	
result1 = []
result2 =[]

swlist = []

cosim = {}
cosimcnt=0
totalcosim = []
listurlword=""
sortlist=[]
top3dic={}
start =0
runtime =0



def process_new_sentence(s):
	sent_list.append(s)
	tokenized = word_tokenize(s)
	for word in tokenized:
		if word not in word_d.keys():
			word_d[word] = 0
		word_d[word] += 1

def make_vector(i):
	v = []
	s = sent_list[i]
	tokenized = word_tokenize(s)
	for w in word_d.keys():
		val = 0
		for t in tokenized:
			if t == w:
				val += 1
		v.append(val)
	return v

def CosineSimilarity(inputurl):
	
	global cosimcnt
	global sent_list
	res1 = ' '.join(result1)
	res2 = ' '.join(result2)
	sent_list=[]
	process_new_sentence(res1)
	process_new_sentence(res2)

	v1 = make_vector(0)
	v2 = make_vector(1)

	dotpro = numpy.dot(v1,v2)
	cossimil = dotpro/float(numpy.linalg.norm(v1)*numpy.linalg.norm(v2))
	cosim = {}
	cosim['urls']= inputurl
	cosim['res'] = cossimil
	totalcosim.append(cosim)
	cosimcnt = cosimcnt+1
	
	#print("dotproduct = ",dotpro)
	#print("Cosine Similarity = ", cossimil)
	#print('')
	#rr= sorted(totalcosim, key=(lambda x: x['res']))
	
	

#def Returntop10(url):
	

def main(url):

	global result1
	global result2
	global sent_list
	global sortlist
	global start
	global start
	global runtime
	global top3dic
	start = time.time()
	url1 = url	#받아와야함
	
	es = Elasticsearch([{'host': es_host, 'port':es_port}], timeout= 30)
	

	#버튼 눌린 url크롤링하기 -> stopwords제거
	res1 = cr.crawling(url1)
	swlist = []
	for sw in stopwords.words("english"):
		swlist.append(sw)
	tokenized1 = word_tokenize(res1)

	for w in tokenized1:
		if w not in swlist:
			result1.append(w)
	
	
	 # 엘라스틱 서치에서 모든 URL을 읽어와서 alldata에 담기
	temp = {}
	query = {"query": {"bool": {"must":[{"match": {"flag": 1}}]}}}
	docs = es.search(index= 'word', body = query, size = 10)
	# print(type(docs['hits']['total']['value']))
	if docs['hits']['total']['value'] > 0:
		for doc in docs['hits']['hits']:
			listurlword = ' '.join(doc['_source']['words'])
			result2 = []
			tokenized1 = word_tokenize(listurlword)

			for w in tokenized1:
				if w not in swlist:
					result2.append(w)
			CosineSimilarity(doc['_source']['url'])
	key=[]
	sortlist= sorted(totalcosim, key=(lambda x: x['res']))
	#print(type(sortlist))
	reverselist=list(reversed(sortlist))
	#print(reverselist)
	
	top3dic = dict(zip(range(len(reverselist)), reverselist))
	del(top3dic[0])
	
	for i in range(len(sortlist)):
		if i>3:
			del(top3dic[i])
	runtime = time.time()-start
	
	
	#print(top3dic)
	


#if __name__ == '__main__':
#	url = "http://climate.apache.org/"
#	main(url)
	#print("______________________________________")


#https://ofbiz.apache.org/
#https://accumulo.apache.org/
#https://calcite.apache.org/
#http://river.apache.org/
#http://ws.apache.org/
#http://oodt.apache.org/
#http://climate.apache.org/


	
	
	

	
