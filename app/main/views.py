#coding:UTF-8

from flask import render_template

from . import main

@main.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@main.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html')


