from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

import crawling as cr
import CosineSim as cs
#import datalist as dt
import tf_idf as tf

es_host = "127.0.0.1"
es_port = "9200"

app = Flask(__name__)
Bootstrap(app)
es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)

data_list = {}
do_function = 0
do_function2 = 0
count = 0
success = "success : url inserted"
success2 = "success : cosine similarity function"
error0 = "fail : invalid url"
error1 = "fail : duplicate URL"
error2 = "fail : file has duplicate url"
error3 = "fail : invalid file"
error4 = "fail : can't found url in database"

@app.route("/")
def index():
    return render_template('index.html', data_list=data_list, state="...", cosinedata=cs.top3dic, wordsdata=tf.top10dic)

@app.route('/insert_data', methods=['POST'])
def insert_data():
    error = None
    if request.method == 'POST':	
        global data_list
        global count
        global do_function
        global do_function2
        do_function = 0
        do_function2 = 0
        # url 받아오기 
        url = request.form['url']
        if url == "":
           #dt.processdata()
          # data_list = dt.esdata_list
           return render_template("index.html", data_list=data_list, state=error0, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)
        if count != 0:
           # dt.processdata()
           # data_list = dt.esdata_list
            for key in data_list:
                if data_list[key]["url"] == url:
                    return render_template("index.html", data_list=data_list, state=error1, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)

        # 크롤링
        #print("url: ", url)
        cr.main(url)
        #print(result1)

        # 엘라스틱 서치에 데이터 넣기
        #print("app.py: " ,len(cr.result1))
        data = {}
        data["url"] = url
        data["time"] = 0
        data["count"] = len(cr.result1)
        # print(data)
        data["words"] = cr.result1
        data["flag"] = 1
        data_list[count] = data
        count = count + 1
       # print(data)

        cr.result1 = []
        cr.temp1 = []
        cr.temp2 = []
        cr.l = ""
        cr.line1 = ""
        cr.line2 = ""
        cr.word_d = {}
        cr.sent_list = []
        res = es.index(index='word', doc_type='url_Data', body=data)

        # print(data_list)

        #dt.processdata()
       # data_list = dt.esdata_list
                
        return render_template('index.html', data_list=data_list, state=success, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)

@app.route('/insert_file', methods=['POST'])
def insert_file():
    error = None
    if request.method == 'POST':
        global count
        global data_list
        global do_function
        global do_function2
        do_function = 0
        do_function2 = 0

        f = request.files['file1']
        if f.filename == '':
           # dt.processdata()
           # data_list = dt.esdata_list
            return render_template("index.html", data_list=data_list, state=error3, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)
        f.save(secure_filename(f.filename))

        file = open(f.filename, 'r')
        line = file.readline()
        while line:
            line.replace(" ", "")
            if count != 0:
              #  dt.processdata()
              #  data_list = dt.esdata_list
                for key in data_list:
                    if (data_list[key]["url"] == line.rstrip('\n')):
                        return render_template("index.html", data_list=data_list, state=error2, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)
            # print(line)
            cr.main(line.rstrip('\n'))
            
            data = {}
            data["url"] = line.rstrip('\n')
            data["time"] = 0
            data["count"] = len(cr.result1)
            # print(data)
            data["words"] = cr.result1
            data["flag"] = 1
            data_list[count] = data
            count = count + 1

            cr.result1 = []
            cr.temp1 = []
            cr.temp2 = []
            cr.l = ""
            cr.line1 = ""
            cr.line2 = ""
            cr.word_d = {}
            cr.sent_list = []
            res = es.index(index='word', doc_type='url_Data', body=data)

            line = file.readline()

       # dt.processdata()
       # data_list = dt.esdata_list
        return render_template('index.html', data_list=data_list, state=success, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)

@app.route('/words_func', methods=['POST'])
def words_func():
    error = None
    if request.method == "POST":
        global do_function
        global do_function2
        do_function = 0
        do_function2 = 0
        words_url = request.form['wordurl']
        length = len(words_url)
        this_url = words_url[2:length-2]

        tf.main(this_url)

        for key in data_list:
            if (data_list[key]["url"] == this_url):
                data_list[key]["time"] = cs.runtime
                query = {"query": {"bool": {"must": [{"match": {"flag": 1}}]}}}
                docs = es.search(index='word', body=query, size=10)
                if docs['hits']['total']['value'] > 0:
                    for doc in docs['hits']['hits']:
                        if doc['_source']['url'] == this_url:
                            doc['_source']['time'] = cs.runtime
                            print(doc['_source']['time'])
                            break
              #  dt.processdata()
              #  data_list = dt.esdata_list
                do_function2 = 1
                print(cs.top3dic)
                return render_template('index.html', data_list=data_list, state=success2, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)
      #  dt.processdata()
      #  data_list = dt.esdata_list
        return render_template('index.html', data_list=data_list, state=error4, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)

        


@app.route('/cosine_func/result')
def cosine_result():
    return render_template('cosine_popup.html', data_list=data_list, state=success2, check=do_function, check2=do_function2, cosinedata=cs.top3dic)

@app.route('/cosine_func', methods=['POST'])
def cosine_func():
    error = None
    if request.method == "POST":
        global do_function
        global do_function2
        do_function = 0
        do_function2 = 0
        print("실행중")
        cosine_url = request.form['cosurl']
        check_url = cosine_url
        length = len(cosine_url)
        this_url = cosine_url[2:length-2]
        print(this_url)
        print(type(this_url))

        cs.main(this_url)

        for key in data_list:
            if (data_list[key]["url"] == this_url):
                data_list[key]["time"] = cs.runtime
                query = {"query": {"bool": {"must": [{"match": {"flag": 1}}]}}}
                docs = es.search(index='word', body=query, size=10)
                if docs['hits']['total']['value'] > 0:
                    for doc in docs['hits']['hits']:
                        if doc['_source']['url'] == this_url:
                            doc['_source']['time'] = cs.runtime
                            print(doc['_source']['time'])
                            break
              #  dt.processdata()
              #  data_list = dt.esdata_list
                do_function = 1
                print(cs.top3dic)
                return render_template('index.html', data_list=data_list, state=success2, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)
      #  dt.processdata()
      #  data_list = dt.esdata_list
        return render_template('index.html', data_list=data_list, state=error4, check=do_function, check2=do_function2, cosinedata=cs.top3dic, wordsdata=tf.top10dic)
