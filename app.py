from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

import crawling as cr

es_host = "127.0.0.1"
es_port = "9200"

app = Flask(__name__)
es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)

data_list = {}
count = 0
inuk = 1

@app.route("/")
def index():
    return render_template('index.html', data_list=data_list)

@app.route('/insert_data', methods=['POST'])
def insert_data():
    error = None
    if request.method == 'POST':	

        global count
        global inuk
        # url 받아오기 
        url = request.form['url']
        if url == "":
           inuk = 2
           return render_template("index.html", data_list=data_list, inuk=inuk)
        if count != 0:
            for key in data_list:
                if data_list[key]["url"] == url:
                    inuk = 2
                    return render_template("index.html", data_list=data_list, inuk=inuk)

        # 크롤링
        cr.main(url)

        # 엘라스틱 서치에 데이터 넣기
        data = {}
        data["url"] = url
        data["time"] = 0
        data["count"] = len(cr.result1)
        data["words"] = cr.result1
        data["flag"] = 1
        data_list[count] = data
        count = count + 1
        res = es.index(index='word', doc_type='url_Data', body=data)
                
        return render_template('index.html', data_list=data_list, inuk=inuk)

# @app.route('/words_func', methods=['POST'])
# def words_func():
#     error = None
#     if request.method == "POST":

@app.route('/cosine_func', methods=['POST'])
def cosine_func():
    error = None
    if request.method == "POST":
        url = request.form['cosurl']
        return render_template('index.html', data_list=data_list, inuk=inuk)
