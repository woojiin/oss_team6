#!/bin/bash

#필요한 파일들을 홈디렉토리로 이동 

cp -r __pycache__ ~/
cp -r env ~/
cp -r static ~/
cp -r templates ~/
cp CosineSim.py ~/
cp README.md ~/
cp app.py ~/
cp crawling.py ~/
cp datalist.py ~/
cp els.es ~/
cp tf_idf.py ~/
cp word_analyze.py ~/

cd ~/
#홈디렉토리에서 team6파일 만들고 team6파일에 필요한 파일 복사하기
mkdir OSP_Team6


mv __pycache__ ~/OSP_Team6
mv env ~/OSP_Team6
mv static ~/OSP_Team6
mv templates ~/OSP_Team6
mv CosineSim.py ~/OSP_Team6
mv README.md ~/OSP_Team6
mv app.py ~/OSP_Team6
mv crawling.py ~/OSP_Team6
mv datalist.py ~/OSP_Team6
mv els.es ~/OSP_Team6
mv tf_idf.py ~/OSP_Team6
mv word_analyze.py ~/OSP_Team6

cd ~/

cd OSP_Team6

echo "설치를 시작합니다."

pip install flask
echo "flask 설치를 완료했습니다."

pip install beautifulsoup4
echo "beautifulsoup4 설치를 완료했습니다."

pip install nltk
echo "nltk 설치를 완료했습니다."

pip install flask-bootstrap
echo "flask-bootstrap 설치를 완료했습니다."

pip install elasticsearch
echo "elasticsearch 설치를 완료했습니다."

pip install requests
echo "requests 설치를 완료했습니다."

pip install numpy
echo "numpy 설치를 완료했습니다."

flask run


