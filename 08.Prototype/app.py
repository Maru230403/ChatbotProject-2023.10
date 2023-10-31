from flask import Flask, render_template, request, flash, session
from bp.crawling import crawl_bp
from bp.map import map_bp
from bp.user import user_bp
from bp.chatbot import chatbot_bp
from bp.schedule import schdedule_bp
from bp.dictionary import dictionary_bp
from bp.mapapi import mapapi_bp
from bp.fraud import fraud_bp
import os, random
import util.map_util as mu
import util.weather_util as wu
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'

app.register_blueprint(crawl_bp, url_prefix='/crawling')    #localhost:5000/crawling/* 는 crawl bp가 처리
app.register_blueprint(map_bp, url_prefix='/map') 
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
app.register_blueprint(schdedule_bp, url_prefix='/schedule')
app.register_blueprint(dictionary_bp, url_prefix='/dictionary')
app.register_blueprint(fraud_bp, url_prefix='/fraud')
app.register_blueprint(mapapi_bp, url_prefix='/mapapi')



@app.before_first_request
def before_first_request():             #최초 1회 실행
    global quotes, quote, addr
    filename = os.path.join(app.static_folder, 'data/todayQuote.txt')
    with open(filename, encoding='utf-8') as file:
        quotes = file.readlines()
    quote = random.sample(quotes, 1)[0]
    session['quote'] = quote
    session['addr'] = '서울시 영등포구'

# for AJAX #######################################
@app.route('/change_quote')
def change_quote():
    quote = random.sample(quotes, 1)[0]
    session['quote'] = quote
    return quote

@app.route('/change_addr')
def change_addr():
    addr = request.args.get('addr')
    session['addr'] = addr
    return addr

@app.route('/weather')
def weather():
    # 서울시 영등포구 + '청' -> 도로명 주소 -> 카카오 로컬 -> 좌표 획득
    addr = request.args.get('addr') 
    lat, lng = mu.get_coord(app.static_folder, addr + '청')
    html = wu.get_weather(app.static_folder, lat, lng)
    return html



##################################################

@app.route('/')
def home():
    menu = {'ho':1, 'us':0, 'cr':0, 'ma':0, 'sc':0}
    #flash('Welcome to my Web!!!')
    return render_template('home.html', menu=menu)

##################################################

def get_naver_news_title():
    url = 'https://land.naver.com/news/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    naver_newstitle = soup.select_one('.group .news_list dt span').get_text()
    news_title_tag = soup.select_one('.group .news_list dt a')
    news_url = news_title_tag['href']
    return naver_newstitle, news_url



@app.route('/get_news_title')
def get_news_title():
    news_title, news_url = get_naver_news_title()
    return {'news_title': news_title, 'news_url': 'https://land.naver.com/' + news_url}

def inject_news_title():
    news_title = get_naver_news_title()
    return dict(news_title=news_title)

if __name__ == '__main__':
    app.run(debug=True)