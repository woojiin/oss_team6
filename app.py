from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

import crawling as cr

es_host = "127.0.0.1"
es_port = "9200"

app = Flask(__name__)
es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/insert_data', methods=['POST'])
def insert_data():
    error = None
    if request.method == 'POST':
        data_list = {}
        count = 0
        inuk = 1

        # url 받아오기 
        url = request.form['url']

        # 크롤링
        cr.main(url)

        # 엘라스틱 서치에 데이터 넣기
        data = {}
        data["url"] = url
        data["time"] = 0
        data["count"] = len(cr.result1)
        data["words"] = cr.result1
        data["flag"] = 1
        res = es.index(index='word', doc_type='url_Data', body=data)

        # 엘라스틱 서치에서 모든 URL을 읽어와서 data_list에 담기
        temp = {}
        query = {"query": {"bool": {"must":[{"match": {"flag": 1}}]}}}
        docs = es.search(index= 'word', body = query, size = 10)
        if docs['hits']['total']['value']>0:
            for doc in docs['hits']['hits']:
                temp["url"] = doc['_source']['url']
                temp["time"] = doc['_source']['time']
                temp["count"] = doc['_source']['count']
                temp["words"] = doc['_source']['words']
                data_list[count] = temp
                count = count + 1

        #print(data_list)
        for key in data_list:
            print(key)
            print(data_list[key])
            if data_list[key]["url"] == url:
                inuk = 2
                return render_template("index.html", data_list=data_list, inuk=inuk)

        return render_template('index.html', data_list=data_list, inuk=inuk)

# @app.route('/words_func', methods=['POST'])
# def words_func():
#     error = None
#     if request.method == "POST":

# @app.route('/cosine_func', methods=['POST'])
# def cosine_func():
#     error = None
#     if request.method == "POST":
