from flask import session, redirect, url_for, render_template, request

from jinja2 import TemplateNotFound
import config
import os, time, cv2
from flask_restplus import Api, Resource, Namespace
from flask import send_file
import numpy as np

from . import mod, namespace
from flask import Response

from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
from pandas import ExcelWriter



def save_xls(list_dfs, xls_path, _list_indexs):
    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            df.to_excel(writer, '%s' % str(_list_indexs[n])[:30])
        writer.save()

@namespace.route('/api_twitter', methods=['GET', 'POST'])
class api_twitter(Resource):
    def get(self):
        return Response(render_template('api_twitter.html'), 200,
                        mimetype='text/html')