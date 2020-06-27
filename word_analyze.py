#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import math
from nltk import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tkinter import *
from tkinter import messagebox


word_d={}
sent_list=[]

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
		tf_d[word]=float(cnt/len(bow))

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
			if cnt ==0:
				continue;				
				#print("나누기가 0")
			else:
				idf_d[t] = float(math.log(Dval/cnt))
	return idf_d

if __name__=='__main__':
	result = []
	url = u'http://abdera.apache.org/'
	res =requests.get(url)

	soup = BeautifulSoup(res.content, "html.parser")

	tags_body = soup.find(id="content").get_text().lower()

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

	process_new_sentence(str_result) #여기에 result를 넣어줘야

	idf_d = compute_idf()
	for i in range(0, len(sent_list)):
		tf_d = compute_tf(sent_list[i])

		tf_idf=tf_d.copy()
		for key, value in tf_idf.items():
		    tf_idf[key]=tf_idf[key]*idf_d[key]
		
		d=Counter(tf_idf)
#		d.most_common()
#		print(type(d))
		#print(d.most_common(10))
		for k, v in d.most_common(10):
			print (k)
		
		print("    ")

	
