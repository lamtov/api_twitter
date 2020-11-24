import importlib, os, sys, time, cv2, base64, traceback, json, _thread
from time import sleep
from datetime import datetime
import numpy as np
from multiprocessing import Process, Manager
from flask import Flask, render_template
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
log_config_dir = 'config/logging.conf'
logging.config.fileConfig(log_config_dir, disable_existing_loggers=False)

Payload.max_decode_packets = 500
app = Flask(__name__)
api = Api(app)
app.config.from_object(config.Config)



### FOR FLASK BLUE PRINT
def register_all_module_controller():
    d = './controllers'
    list_dir = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    print(list_dir)
    for module in list_dir:
        module_page = importlib.import_module('controllers.' + str(module))
        app.register_blueprint(module_page.mod)


def register_module(module_name, url_prefix=None):
    module_page = importlib.import_module('controllers.' + str(module_name))
    if url_prefix is None:
        app.register_blueprint(module_page.mod)
    else:
        app.register_blueprint(module_page.mod, url_prefix=url_prefix)


def register_namespace(api, namespace_name, path=None):
    module_page = importlib.import_module('controllers.' + str(namespace_name))
    if path is None:
        api.add_namespace(module_page.namespace)
    else:
        api.add_namespace(module_page.namespace, path=path)




HOST = '0.0.0.0'  # The server's hostname or IP address
PORT = 3006       # The port used by the server
#executor = ThreadPoolExecutor(1)

# es = Elasticsearch([{'host': '34.126.113.23', 'port': int(9200)}])

# @app.route('/demo_image_frame', methods=['POST'])
# def demo_image_frame():
#     global play
#     play = not play
#     return {"ok": "done"}
from flask_restplus import Api, Resource,Namespace
from flask import Blueprint, abort, request, redirect, url_for
if __name__ == "__main__":
    #
    # executor = ThreadPoolExecutor(1)
    # register_module("test_api")
    # register_module('spec_network')
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api = Api(blueprint,
              title="My API",
              description="My Cool API")
    register_namespace(api,'auto_tweet')
    app.register_blueprint(blueprint)
    app.logger.addHandler(logging.handlers)
    app.run(debug=True,host=HOST, port=PORT)

