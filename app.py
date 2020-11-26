import importlib, os, sys, time, cv2, base64, traceback, json, _thread
from time import sleep
from datetime import datetime
import numpy as np
from multiprocessing import Process, Manager
from engineio.payload import Payload
from flask_socketio import SocketIO
from flask_restplus import Api, Resource, fields
import logging.config
import config
from flask import session
from flask_socketio import emit, join_room, leave_room
import base64
import json
from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from concurrent.futures import ThreadPoolExecutor
from utils.twitterbot import TwitterBot
import flask
from flask_restplus import Api, Resource,Namespace
from flask import Blueprint, abort, request, redirect, url_for,Flask, render_template
from flask import Response
from flask import flash, request, redirect, render_template
from flask_socketio import SocketIO

log_config_dir = 'config/logging.conf'
logging.config.fileConfig(log_config_dir, disable_existing_loggers=False)
Payload.max_decode_packets = 500
app = flask.Flask(__name__)
api = Api(app)
app.config.from_object(config.Config)
center_socketio = SocketIO()
center_socketio.init_app(app)
HOST = '0.0.0.0'  # The server's hostname or IP address
PORT = 5009       # The port used by the server
executor = ThreadPoolExecutor(1)
# list_twitter_bot_users= config.list_twitter_bot_users
# print(list_twitter_bot_users)
#
# list_twitter_bot=[]
#
# def init_twitter_bot(number_threads):
#     #init with number thread and test status of twitter
#     global list_twitter_bot
#     list_twitter_bot=[]
#     for bot_user in list_twitter_bot_users:
#         user_name = bot_user['user_name']
#         password = bot_user['password']
#         t = TwitterBot(user_name, password)
#         list_twitter_bot.append(t)

@app.route('/index', methods=['GET', 'POST'])
def api():
    if flask.request.method == 'POST':
        file_user_data = request.files['file_user_data']
        path_file_user_data=os.path.dirname(sys.modules['__main__'].__file__) + 'file_user_data.txt'
        file_picture = request.files['file_picture']
        path_file_picture=os.path.dirname(sys.modules['__main__'].__file__)+'picture.jpg'

        file_proxy = request.files['file_proxy']
        path_file_proxy=os.path.dirname(sys.modules['__main__'].__file__)+'file_proxy.txt'

        file_user_data.save(path_file_user_data)
        file_picture.save(path_file_picture)
        file_proxy.save(path_file_proxy)

        number_threads = request.form['number_threads']
        spam_message = request.form['spam_message']

        list_user_data=open(path_file_user_data, encoding="utf8").readlines()
        list_proxy=open(path_file_proxy, encoding="utf8").readlines()
        list_twitter_bot_users = config.list_twitter_bot_users




        return Response(render_template('index.html'), 200,
                        mimetype='text/html')
    else:
        return Response(render_template('index.html'), 200,
                        mimetype='text/html')


spam_infos={'number_users_spam':0, 'number_posts_spam':0, 'number_locked_spam':0}

@app.route('/test', methods=['GET', 'POST'])
def test1():
    if flask.request.method == 'POST':
        return redirect(request.url)
    else:
        global spam_infos
        spam_infos['number_users_spam']=spam_infos['number_users_spam']+1
        spam_infos['number_posts_spam'] = spam_infos['number_posts_spam'] + 2
        spam_infos['number_locked_spam'] = spam_infos['number_locked_spam'] + 3
        center_socketio.emit('update_spam_infos', spam_infos, broadcast=True, namespace='/spam_infos')
        return {"ok": "ok"}







@app.route('/api/api_twitter', methods=['GET', 'POST'])
def api_twitter():
    if flask.request.method == 'POST':
        file_user_data = request.files['file_user_data']
        file_picture = request.files['file_picture']
        file_picture_dir=os.path.dirname(sys.modules['__main__'].__file__)+'picture.jpg'
        file_picture.save(file_picture_dir)
        file_proxy = request.files['file_proxy']
        number_threads = request.form['number_threads']
        list_twitter_bot[0].TweetSomething('hello @LamVna', file_picture_dir)
        flash("START ")

        return redirect(request.url)
    else:
        return Response(render_template('api_twitter.html'), 200,
                        mimetype='text/html')



if __name__ == "__main__":
    #
    # executor.submit(init_twitter_bot)
    app.logger.addHandler(logging.handlers)
    # app.run(debug=True,host=HOST, port=PORT)
    center_socketio.run(app, host="0.0.0.0", port=5009, debug=True, log_output=True), ()
