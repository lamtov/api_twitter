from flask import session, redirect, url_for, render_template, request

from jinja2 import TemplateNotFound
import config
import os, time, cv2
from flask_restplus import Api, Resource, Namespace
from flask import send_file
import numpy as np
from flask import flash, request, redirect, render_template
from . import mod, namespace
from flask import Response

from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from app import list_twitter_bot



def save_xls(list_dfs, xls_path, _list_indexs):
    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):l
            df.to_excel(writer, '%s' % str(_list_indexs[n])[:30])
        writer.save()

@namespace.route('/api_twitter', methods=['GET', 'POST'])
class api_twitter(Resource):
    def get(self):
        return Response(render_template('api_twitter.html'), 200,
                        mimetype='text/html')
    def post(self):
        file_user_data = request.files['file_user_data']
        file_picture = request.files['file_picture']
        file_proxy=request.files['file_proxy']
        number_threads = request.form['number_threads']
        list_twitter_bot[0].TweetSomething('hello @LamVna',file_picture)
        flash("START " )

        return redirect(request.url)