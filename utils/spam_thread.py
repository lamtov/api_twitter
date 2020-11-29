from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import click
import traceback
import random
import string
from utils.twitterbot import  TwitterBot
from global_assets.common import get_random_string
import datetime

class SpamThread():
    def __init__(self, database):
        try:
            self.database=database
            self.status="INIT"
            self.target_index=0
            self.list_target=None
            self.proxy=None
            self.spam_message =None
            self.spam_picture = None
            self.running_bot=None

        except Exception as e:
            self.status=str(traceback.format_exc())

    def get_next_running_bot(self):
        time.sleep(0.2)
        bot = None
        while bot is None or bot.status != 'OK':
            bot = self.database.get_next_running_bot()
            if bot is None:
                time.sleep(60)
            else:
                bot.signIn(self.proxy)
                while bot.status=='PROXY_FAILED':
                    self.proxy=self.database.get_next_proxy()
                    bot.signIn(self.proxy)

                if bot.status == 'OK':
                    bot.check_block()
                    if bot.status == 'OK':
                        return bot
                    else:
                        bot.close()
                else:
                    bot.close()

        return bot

    def set_value(self):
        self.dir=self.database.get_next_dir()
        self.dir.status='RUNNING'
        self.list_target = self.dir._list_user_data
        self.spam_message = self.dir.message
        self.spam_picture = self.dir.file_picture
        self.proxy = self.database.get_next_proxy()
        if self.running_bot is None or self.running_bot.status!='OK':
            self.running_bot = self.get_next_running_bot()

    def do_thread(self):
        self.set_value()
        while self.dir is not None:
        # self.dir.target_index =0
            self.dir.status='RUNNING'
            while self.dir.target_index < len(self.list_target):
                targets=self.list_target[self.dir.target_index:self.dir.target_index+24]
                _list_mention=targets[0:14]
                _list_tags=targets[14:]
                message = self.spam_message
                for target_mention in _list_mention:
                    message = message + '\n @' + target_mention + ' '
                if self.running_bot.status!='OK':
                    try:
                        self.running_bot.close()
                    except:
                        print('close')
                    self.running_bot=self.get_next_running_bot()

                _list_tagged =self.running_bot.TweetSomething(self.spam_message,_list_mention,self.spam_picture, _list_tags)
                _num_target_spam=len(_list_tagged)
                if _num_target_spam > 0:
                    self.dir.number_post=self.dir.number_post+1
                    self.dir.status='RUNNING'
                    self.dir.target_index=self.dir.target_index+24
                    self.dir.num_target_spam=self.dir.num_target_spam+_num_target_spam
                    self.dir.write_user_spam(_list_tagged)
                else:
                    self.dir.status = 'ERROR'

            self.dir.status='DONE'
            self.set_value()






if __name__ == "__main__":
    # username = click.prompt("Enter the number", type=str, default="anvien01111995@gmail.com")
    # password = click.prompt("Enter the number", type=str, default="To01111995")

    list_user_spam=[
        {'username': 'lane287279070', 'password': 'To01111995'}]
    list_target=['ahmedbader1989rest_id', 'akhil_prabha', 'xo_generation']
    list_proxy=['127.0.0.1', '127.0.0.1', '127.0.0.1']
    spam_message='Spam Message'
    spam_picture='C:/Users/etoxlam/Documents/python_project/api_twitterpicture.jpg'

    spam_thread=SpamThread(list_user_spam, list_target,list_proxy, spam_message, spam_picture)
    spam_thread.do_thread()
