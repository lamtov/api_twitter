from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import click
import traceback
import random
import string
from utils.twitterbot import TwitterBot
from global_assets.common import get_random_string
import datetime
from utils.twitterbot import TwitterBot
from utils.spam_thread import SpamThread
import os
from threading import Lock


class Dir():
    def __init__(self, data_dir):
        try:
            data_dir = data_dir.replace('\\', '/')
            self.data_user_spam=data_dir + '/' + 'user_spam.txt'
            self.name=data_dir.split('/')[-1]
            self.status = 'init'
            self.target_index = 0
            self.number_post = 0
            self.num_target_spam=0
            self.message = str(open(data_dir + '/' + 'content.txt', encoding="utf8").read())
            self._list_user_data = open(data_dir + '/' + 'data.txt', encoding="utf8").readlines()[:]
            self.file_picture = data_dir + '/' + 'mockup.jpg'
        except Exception as e:
            self.target_index = 0
            self.number_post = 0
            self.num_target_spam=0
            self.status = str('ERROR')
    def write_user_spam(self,_list_tagged):
        with open(self.data_user_spam , 'a',encoding="utf8") as filehandle:
            for username in _list_tagged:
                filehandle.write(username+'\n')


class DataBase():
    def __init__(self, list_twitter_bot_users, file_user_data, list_proxy, number_threads):
        try:
            self.list_twitter_bot_users = list_twitter_bot_users
            self.list_dirs = []
            self.list_bot = []
            for user_spam in list_twitter_bot_users:
                user_bot = TwitterBot(user_spam['username'], user_spam['password'])
                self.list_bot.append(user_bot)
            subdirs = [x[0] for x in os.walk(file_user_data)]
            for dir in subdirs[1:]:
                user_data = Dir(dir)
                self.list_dirs.append(user_data)
            self.list_proxy = list_proxy
            self.list_spam_threads = []
            self.list_twitter_bot_users = []
            self.idx_thread = 0
            self.isLogging = False
            self.lock_1 = Lock()
            self.lock_2 = Lock()
            self.lock_3 = Lock()
            self.lock_4 = Lock()


        except Exception as e:
            self.status = str('ERROR')

    def get_next_running_bot(self):
        self.lock_1.acquire()
        try:
            for bot in self.list_bot:
                if bot.status == 'init':
                    bot.status = 'OK'
                    return bot
            for bot in self.list_bot:
                if bot.status == 'BLOCKING'  :
                    if bot.start_block is None:
                        bot.start_block=datetime.datetime.now()
                    time_block = (datetime.datetime.now() - bot.start_block).total_seconds()
                    if time_block > 1800:
                        bot.start_block = datetime.datetime.now()
                        bot.status = 'OK'
                        return bot
        finally:
            self.lock_1.release()
        return None

    def get_next_proxy(self):
        self.lock_3.acquire()
        try:
            if len(self.list_proxy) ==0:
                return  None

            proxy=self.list_proxy[0]
            self.list_proxy.pop(0)
            return  proxy
        finally:
            self.lock_3.release()
        return None

    def get_next_dir(self):
        self.lock_2.acquire()
        try:
            for dir in self.list_dirs:
                if dir.status == 'init':
                    return dir
        finally:
            self.lock_2.release()
        return None
