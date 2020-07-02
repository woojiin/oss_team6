from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from werkzeug.utils import secure_filename

import crawling as cr

es_host = "127.0.0.1"
es_port = "9200"

app = Flask(__name__)
es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)

data_list = {}
count = 0
success = "success : url inserted"
success2 = "success : cosine similarity function"
error0 = "fail : invalid url"
error1 = "fail : duplicate URL"
error2 = "fail : file has duplicate url"
error3 = "fail : invalid file"

@app.route("/")
def index():
    return render_template('index.html', data_list=data_list, state="...")

@app.route('/insert_data', methods=['POST'])
def insert_data():
    error = None
    if request.method == 'POST':	

        global count
        # url 받아오기 
        url = request.form['url']
        if url == "":
           return render_template("index.html", data_list=data_list, state=error0)
        if count != 0:
            for key in data_list:
                if data_list[key]["url"] == url:
                    return render_template("index.html", data_list=data_list, state=error1)

        # 크롤링
        cr.main(url)

        # 엘라스틱 서치에 데이터 넣기
        data = {}
        data["url"] = url
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

        # print(data_list)
                
        return render_template('index.html', data_list=data_list, state=success)

@app.route('/insert_file', methods=['POST'])
def insert_file():
    error = None
    if request.method == 'POST':
        global count

        f = request.files['file1']
        if f.filename == '':
            return render_template("index.html", data_list=data_list, state=error3)
        f.save(secure_filename(f.filename))

        file = open(f.filename, 'r')
        line = file.readline()
        while line:
            line.replace(" ", "")
            if count != 0:
                for key in data_list:
                    if (data_list[key]["url"] == line.rstrip('\n')):
                        return render_template("index.html", data_list=data_list, state=error2)
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

        return render_template('index.html', data_list=data_list, state=success)

# @app.route('/words_func', methods=['POST'])
# def words_func():
#     error = None
#     if request.method == "POST":

@app.route('/cosine_func', methods=['POST'])
def cosine_func():
    error = None
    if request.method == "POST":
        print("실행중")
        cosine_url = request.form['cosurl']
        length = len(cosine_url)
        this_url = cosine_url[2:length-2]
        print(this_url)
        for key in data_list:
            if (data_list[key]["url"] == this_url):
                data_list[key]["time"] = 111
                return render_template('index.html', data_list=data_list, state=success2)
        return render_template('index.html', data_list=data_list, state=success2)
