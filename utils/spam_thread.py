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
    def __init__(self, list_user_spam, list_target,list_proxy, spam_message, spam_picture):
        try:
            self.status="RUNNING"
            self.list_bot=[]
            for user_spam in list_user_spam:
                user_bot = TwitterBot(user_spam['username'], user_spam['password'])
                self.list_bot.append(user_bot)
            self.target_index=0
            self.list_target=list_target
            self.list_proxy=list_proxy
            self.spam_message =spam_message
            self.spam_picture = spam_picture
            self.running_bot=None
        except Exception as e:
            self.status=str(traceback.format_exc())

    def get_next_running_bot(self):
        for bot in self.list_bot:
            if bot.status=='init':
                bot.signIn()
                bot.check_block()
                if bot.status=='OK':
                    return bot
        for bot in self.list_bot:
            if bot.status=='BLOCKING':
                time_block=(datetime.datetime.now() - bot.start_block).total_seconds()
                if time_block>3600:
                    bot.signIn()
                    bot.check_block()
                    if bot.status=='OK':
                        return bot
        return {'status':"NONE"}


    def to_json(self):
        for bot in self.list_bot:
            print(bot.to_json())
        print(self.target_index)
        print(self.list_target)
        print(self.list_proxy)
        print(self.status)
        print(self.spam_message)
        print(self.spam_picture)
    def do_thread(self):
        self.running_bot=self.get_next_running_bot()
        while self.target_index < len(self.list_target):
            targets=self.list_target[self.target_index:self.target_index+10]
            message = self.spam_message
            for target in targets:
                message= message+' @'+target+' '
            while self.running_bot.status!='OK':
                self.running_bot=self.get_next_running_bot()
                if self.running_bot.status=='NONE':
                    time.sleep(60)

            self.running_bot.TweetSomething(message,self.spam_picture)
            self.target_index=self.target_index+10




if __name__ == "__main__":
    # username = click.prompt("Enter the number", type=str, default="anvien01111995@gmail.com")
    # password = click.prompt("Enter the number", type=str, default="To01111995")

    list_user_spam=[{'username': 'anvien01111995@gmail.com', 'password': 'To01111995'},
        {'username': 'lane287279068', 'password': 'To01111995'},
        {'username': 'lane287279069', 'password': 'To01111995'},
        {'username': 'lane287279070', 'password': 'To01111995'}]
    list_target=['ahmedbader1989rest_id', 'akhil_prabha', 'xo_generation']
    list_proxy=['127.0.0.1', '127.0.0.1', '127.0.0.1']
    spam_message='Spam Message'
    spam_picture='C:/Users/etoxlam/Documents/python_project/api_twitterpicture.jpg'

    spam_thread=SpamThread(list_user_spam, list_target,list_proxy, spam_message, spam_picture)
    spam_thread.do_thread()
