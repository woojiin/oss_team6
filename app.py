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

        data_list[count] = temp
        count = count + 1

        return render_template('index.html', data_list=data_list)

# @app.route('/words_func', methods=['POST'])
# def words_func():
#     error = None
#     if request.method == "POST":

# @app.route('/cosine_func', methods=['POST'])
# def cosine_func():
#     error = None
#     if request.method == "POST":
