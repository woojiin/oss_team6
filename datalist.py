#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import re

from flask import Flask, render_template
from elasticsearch import Elasticsearch

es_host = "127.0.0.1"
es_port = "9200"
esdata={}
esurl = ""
estime=0
escount=0
eswords=[]
esflag=1
esdata_list = {}
escount=0

es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)

def processdata():
	global escount
	global esdata 
	global esdata_list
	esdata = {}
	esdata_list = {}
	escount = 0
	temp = {}
	query = {"query": {"bool": {"must":[{"match": {"flag": 1}}]}}}
	docs = es.search(index= 'word', body = query, size = 10)
	#print(type(docs['hits']['total']['value']))
	if docs['hits']['total']['value']>0:	
		for doc in docs['hits']['hits']:
			esdata["url"] = doc['_source']['url']
			esdata["time"] = doc['_source']['time']
			esdata["count"] = doc['_source']['count']
			esdata["words"] = doc['_source']['words']
			esdata["flag"] = doc['_source']['flag']
			esdata_list[escount] = esdata
			esdata = {}
			#print(esdata)
			#print("")
			escount +=1
	
	print(esdata_list)


#if __name__ == '__main__':
#	processdata()
