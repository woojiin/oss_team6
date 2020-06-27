#!/usr/bin/python
#-*- coding: utf-8 -*-


import sys
import re
import requests
import nltk
import numpy

nltk.download('punkt')
nltk.download('stopwords')
from bs4 import BeautifulSoup
from flask import Flask, render_template
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

temp1 = []
temp2 = []
l = ""
line1 = ""
line2 = ""
word_d ={}
sent_list = []

def crawling(url):
	#es = Elasticsearch([{'host': es_host, 'port':es_port}], timeout= 30)
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
	return line1.lower()

def main(url):
	url1 = url
	
	res1 = crawling(url1)
	
	swlist = []

	for sw in stopwords.words("english"):
		swlist.append(sw)
	tokenized1 = word_tokenize(res1)
	
	result1 = []

	for w in tokenized1:
		if w not in swlist:
			result1.append(w)

	print(result1)
	
if __name__ == '__main__':
	url = "https://en.wikipedia.org/wiki/Web_crawler"
	main(url)

	


	
