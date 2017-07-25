#coding:UTF-8

from flask import render_template

from . import main

@main.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@main.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html')


@main.route('/channel', methods=['GET','POST'])
def channel():
    return render_template('channel.html')

@main.route('/map', methods=['GET','POST'])
def map():
    return render_template('map.html')
