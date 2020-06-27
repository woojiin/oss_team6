#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import re
import requests
import nltk
import numpy
<<<<<<< HEAD
=======
import crawling


>>>>>>> ac1c9b6ab78c2389c66e692a5c7116a3cae7b7d8
nltk.download('punkt')
nltk.download('stopwords')
from bs4 import BeautifulSoup
from flask import Flask, render_template
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import crawling as cr

ee_host = "127.0.0.1"
ee_port = "9200"
temp1 = []
temp2 = []
l = ""
line1 = ""
line2 = ""
word_d ={}
<<<<<<< HEAD
sent_list = []


def crawling(url):
	es = Elasticsearch([{'host': ee_host, 'port':ee_port}], timeout= 30)
	request = requests.get(url)

	soup = BeautifulSoup(request.content, 'html.parser')
	body = soup.find_all('body')[0].get_text()
	global l
	global line1
	

	for w in body:
		l += w

	temp1 = l.split()

	for w in temp1:
		w = re.sub('[^\w\s]+', ' ', w)
		temp2.append(w)
	
	temp1 = []

	for w in temp2:
		w = re.sub('[^A-Za-z]+', ' ', w)
		temp1.append(w)
	while ' ' in temp1:
		temp1.remove(' ')
	

	for w in temp1:
		line1 += w
		if w[len(w)-1] == ' ':
			line1 += ''
		else:
			line1 += ' '
	return line1
	
	
=======
sent_list = []	
>>>>>>> ac1c9b6ab78c2389c66e692a5c7116a3cae7b7d8
	

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

if __name__ == '__main__':

	url1 = "http://arrow.apache.org/"
	url2 = "http://arrow.apache.org/"
<<<<<<< HEAD
	res1 = crawling(url1)
	res2 = crawling(url2)
=======
	
	res1 = cr.crawling(url1)
	res2 = cr.crawling(url2)
>>>>>>> ac1c9b6ab78c2389c66e692a5c7116a3cae7b7d8
	swlist = []
	for sw in stopwords.words("english"):
		swlist.append(sw)
	tokenized1 = word_tokenize(res1)
	tokenized2 = word_tokenize(res2)

	result1 = []
	result2 = []
	
	for w in tokenized1:
		if w not in swlist:
			result1.append(w)

	for w in tokenized2:
		if w not in swlist:
			result2.append(w)

<<<<<<< HEAD
	

	#print(len(tokenized))
	#print(len(result))
	
	

	res1 = ' '.join(result1)
	res2 = ' '.join(result2)


	#print(res1)
	#print(res2)
=======
	res1 = ' '.join(result1)
	res2 = ' '.join(result2)

>>>>>>> ac1c9b6ab78c2389c66e692a5c7116a3cae7b7d8
	process_new_sentence(res1)
	process_new_sentence(res2)

	v1 = make_vector(0)
	v2 = make_vector(1)
	
	dotpro = numpy.dot(v1,v2)
	cossimil = dotpro/float(numpy.linalg.norm(v1)*numpy.linalg.norm(v2))

	print("dotproduct = ",dotpro)
	print("Cosine Similarity = ", cossimil)


