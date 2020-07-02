#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import re
import requests
import nltk
import numpy
import crawling
import math
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

count=0

word_d = {}
sent_list = []

result1 = []
result2 =[]

swlist = []
stringres1 = ""
stringres2 =""
totaltfidf = []
top10dic={}
start=0
runtime=0
sortlist =[]



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
	for word, count in wordcount_d.items():
		tf_d[word]=float(count)/len(bow)
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
			
			
			
	#print(idf_d)
	return idf_d

def tfidf():
	global count
	global totaltfidf
	global tdcnt
	idf_d = compute_idf()
	for i in range(0,len(sent_list)):
		tf_d = compute_tf(sent_list[i])
		
		for word, tval in tf_d.items():
			td = {}
			td['word']= word
			td['res'] = tval*idf_d[word]
			totaltfidf.append(td)	

	
				

def main(url):

	global result1
	global result2
	global sent_list
	global sortlist
	global stringres2
	global start
	global runtime
	global top10dic	

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
	stringres1=' '.join(result1)
	process_new_sentence(stringres1)
	
	
	 # 엘라스틱 서치에서 모든 URL을 읽어와서 alldata에 담기
	temp = {}
	query = {"query": {"bool": {"must":[{"match": {"flag": 1}}]}}}
	docs = es.search(index= 'word', body = query, size = 10)

	if docs['hits']['total']['value']>0:	
		for doc in docs['hits']['hits']:
			listurlword = ' '.join(doc['_source']['words'])
			result2 = []
			tokenized1 = word_tokenize(listurlword)

			for w in tokenized1:
				if w not in swlist:
					result2.append(w)
			stringres2=' '.join(result2)
			process_new_sentence(stringres2)
	
	tfidf()
	sortlist= sorted(totaltfidf, key=(lambda x: x['res']))
	
	
	#print(type(sortlist))
	reverselist=list(reversed(sortlist))
	templist=reverselist
	#print(reverselist)
	for i in templist:
		for j in templist:
			if i['word'] == j['word']:
				if i['res']>j['res']:
					reverselist.remove(j)
	i=0
	j=0
	while i<len(reverselist):
		j=0
		while j<len(reverselist):
			#print("1")
			if i<j:
				if reverselist[i]['word']==reverselist[j]['word']:
					if reverselist[i]['res'] == reverselist[j]['res']:
						reverselist.remove(reverselist[j])
			j+=1
		i+=1
	
	#reverselist=list(set(reverselist))
	

				
	#print(reverselist)
	top10dic = dict(zip(range(len(reverselist)), reverselist))
	
	for i in range(len(reverselist)):
		if i>9:
			del(top10dic[i])
	runtime = time.time()-start
	#print(top10dic)
	

#if __name__ == '__main__':
#	url = "http://climate.apache.org/"
#	main(url)

		
