from engineio.payload import Payload

import config

from concurrent.futures import ThreadPoolExecutor

from utils.spam_thread import SpamThread
from utils.database import DataBase
import flask
from flask_restplus import Api, Resource, Namespace

from flask import Response
from flask import flash, request, redirect, render_template
from flask_socketio import SocketIO

log_config_dir = 'config/logging.conf'
# logging.config.fileConfig(log_config_dir, disable_existing_loggers=False)
Payload.max_decode_packets = 500
app = flask.Flask(__name__)
api = Api(app)
app.config.from_object(config.Config)
center_socketio = SocketIO()
center_socketio.init_app(app)
HOST = '0.0.0.0'  # The server's hostname or IP address
PORT = 5009  # The port used by the server

spam_infos = {'number_users_spam': 0, 'number_posts_spam': 0, 'number_locked_spam': 0}
list_spam_threads = []


def do_thread(spam_thread):
    spam_thread.do_thread()


list_twitter_bot_users = [

]
database = None
stop_running="RUNNING"

@app.route('/index', methods=['GET', 'POST'])
def api():
    if flask.request.method == 'POST':
        global list_spam_threads
        global list_twitter_bot_users
        global database
        file_user_twitter = request.form['file_user_twitter'].replace('\\', '/')
        file_list_twitter_bot = open(file_user_twitter, encoding="utf8")
        for line in file_list_twitter_bot.readlines():
            list_twitter_bot_users.append(
                {'username': line.split('|')[0], 'password': line.split('|')[1].replace('\n', '')})
        file_user_data = request.form['file_user_data'].replace('\\', '/')
        file_proxy = request.form['file_proxy'].replace('\\', '/')
        list_proxy = open(file_proxy, encoding="utf8").readlines()[:]
        number_threads = int(request.form['number_threads'])
        database = DataBase(list_twitter_bot_users, file_user_data, list_proxy, number_threads)

        for i in range(0, number_threads):
            spam_thread = SpamThread(database)
            list_spam_threads.append(spam_thread)
            # do_thread(spam_thread)
            executor = ThreadPoolExecutor(1)
            executor.submit(do_thread, spam_thread)
        list_folders = [str(idx) for idx in range(1, len(database.list_dirs) + 1)]
        return Response(render_template('index.html', list_folders=list_folders), 200,
                        mimetype='text/html')
    else:
        list_folders = []
        return Response(render_template('index.html', list_folders=list_folders), 200,
                        mimetype='text/html')


@app.route('/get_spam_infos', methods=['GET', 'POST'])
def get_spam_infos():
    if flask.request.method == 'POST':
        return redirect(request.url)
    else:
        global spam_infos
        spam_infos = {'number_users_spam': 0, 'number_posts_spam': 0, 'number_locked_spam': 0,
                      'number_signin_failse': 0}
        if database is None:
            return spam_infos

        list_bots = database.list_bot
        list_dir = database.list_dirs
        for bot in list_bots:
            if bot.status == 'init':
                spam_infos['number_users_spam'] = spam_infos['number_users_spam'] + 1
            if bot.status == 'LOGIN_FAILED':
                spam_infos['number_signin_failse'] = spam_infos['number_signin_failse'] + 1
            if bot.status == 'BLOCKING':
                spam_infos['number_locked_spam'] = spam_infos['number_locked_spam'] + 1
        for dir in list_dir:
            spam_infos['number_posts_spam'] = spam_infos['number_posts_spam'] + dir.number_post
        return spam_infos


@app.route('/get_dir_infos', methods=['GET', 'POST'])
def get_dir_infos():
    if flask.request.method == 'POST':
        return redirect(request.url)
    else:
        global spam_infos

        spam_infos = {'name': [], 'num_post_': [], 'num_target_spam_': [],
                      'status_': [], 'number_dir': 0}
        if database is None:
            return spam_infos
        list_dir = database.list_dirs

        spam_infos['number_dir'] = len(list_dir)
        for dir in list_dir:
            spam_infos['name'].append(dir.name)
            spam_infos['num_post_'].append(dir.number_post)
            spam_infos['num_target_spam_'].append(dir.num_target_spam)
            spam_infos['status_'].append(dir.status)

        # center_socketio.emit('update_spam_infos', spam_infos, broadcast=True, namespace='/spam_infos')
        return spam_infos



@app.route('/stop_resume', methods=['POST'])
def stop_resume():
    if flask.request.method == 'POST':
        global database
        global stop_running
        if database is None:
            return {'message':"No Thread Running",'flag':'IDLE'}
        else:
            if stop_running=='STOP':
                stop_running='RUNNING'
                for spam_thread in list_spam_threads:
                    spam_thread.STOP=False
                return {'message': "RESUME ALL THREADS",'flag':'RUNNING'}
            else:
                stop_running='STOP'
                for spam_thread in list_spam_threads:
                    spam_thread.STOP=True
                return {'message':"STOP ALL THREADS",'flag':'STOP'}
    else:
        return {'ok':'ok'}



#
# @app.route('/api/api_twitter', methods=['GET', 'POST'])
# def api_twitter():
#     if flask.request.method == 'POST':
#         file_user_data = request.files['file_user_data']
#         file_picture = request.files['file_picture']
#         file_picture_dir=os.path.dirname(sys.modules['__main__'].__file__)+'picture.jpg'
#         file_picture.save(file_picture_dir)
#         file_proxy = request.files['file_proxy']
#         number_threads = request.form['number_threads']
#         # list_twitter_bot[0].TweetSomething('hello @LamVna', file_picture_dir)
#
#         for i in range(0,number_threads):
#
#
#
#         flash("START ")
#
#         return redirect(request.url)
#     else:
#         return Response(render_template('api_twitter.html'), 200,
#                         mimetype='text/html')


if __name__ == "__main__":
    #
    # executor.submit(init_twitter_bot)
    # app.logger.addHandler(logging.handlers)
    app.run(debug=False, host=HOST, port=PORT)
    # center_socketio.run(app, host="0.0.0.0", port=5009), ()
