#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import re
import requests
import nltk
import numpy
import crawling
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
temp1 = []
temp2 = []
l = ""
line1 = ""
line2 = ""
word_d ={}
sent_list = []	
result1 = []
result2 =[]
alldata = {}
swlist = []
count =0
cosim = {}
cosimcnt=0
totalcosim = {}
	
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

def CosineSimilarity(url):
	global cosimcnt
	res1 = ' '.join(result1)
	res2 = ' '.join(result2)

	process_new_sentence(res1)
	process_new_sentence(res2)

	v1 = make_vector(0)
	v2 = make_vector(1)

	dotpro = numpy.dot(v1,v2)
	cossimil = dotpro/float(numpy.linalg.norm(v1)*numpy.linalg.norm(v2))
	cosim['urls']= url
	cosim['res'] = cossimil
	totalcosim[cosimcnt] = cosim
	cosimcnt = cosimcnt+1
	
	print("dotproduct = ",dotpro)
	print("Cosine Similarity = ", cossimil)

def main(url):
	global count
	url1 = url	#받아와야함
	es = Elasticsearch([{'host': es_host, 'port':es_port}], timeout= 30)
	

	#버튼 눌린 url크롤링하기
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
	if docs['hits']['total']['value']>0:	
		for doc in docs['hits']['hits']:	
			temp["url"] = doc['_source']['url']
			temp["words"] = doc['_source']['words']
			alldata[count] = temp
			#print(alldata[count])
			count = count + 1
			
	for i in range(0,count):
		print(alldata[i]['url'])
		res2=cr.crawling(alldata[i]['url'])
		#print(res2)
		#print(type(word_tokenize(res2)))
		for sw in stopwords.words("english"):
			swlist.append(sw)
		tokenized2 = word_tokenize(res2)
		

		for w in tokenized2:
			if w not in swlist:
				result2.append(w)
		CosineSimilarity(alldata[i]['url'])
	print(totalcosim)

	return totalcosim
		
		



if __name__ == '__main__':
	#main(url)
	#print("______________________________________")
	
	
	
	
	

	
