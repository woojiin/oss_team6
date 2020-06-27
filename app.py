from flask import Flask, render_template, request
# from elasticsearch import Elasticsearch

import crawling as cr

es_host = "127.0.0.1"
es_port = "9200"

app = Flask(__name__)
# es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/insert_data', methods=['POST'])
def insert_data():
    error = None
    if request.method == 'POST':
        data_list = {}
        url = request.form['url']
        cr.main(url)
        # data = {
        #     "url" = url,
        #     "time" = 0,
        #     "count" = len(cr.result1),
        #     "words" = cr.result1
        # }
        data = {}
        data["url"] = url
        data["time"] = 0
        data["count"] = len(cr.result1)
        data["words"] = cr.result1
        res = es.index(index='word', doc_type='url_Data', body=data)

        return render_template('index.html', data_list=data_list)

# @app.route('/words_func', methods=['POST'])
# def words_func():
#     error = None
#     if request.method == "POST":

# @app.route('/cosine_func', methods=['POST'])
# def cosine_func():
#     error = None
#     if request.method == "POST":
