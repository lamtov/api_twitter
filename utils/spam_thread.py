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


class SpamThread():
    def __init__(self, list_user_spam, list_target,list_proxy, spam_message, spam_picture):
        try:
            self.status="RUNNING"
            self.list_user_bot=[]
            for user_spam in list_user_spam:
                user_bot = TwitterBot(user_spam['user_name'], user_spam['password'])
                self.list_user_bot.append(user_bot)
            self.target_index=0
            self.list_target=list_target
            self.list_proxy=list_proxy
            self.spam_message =spam_message
            self.spam_picture = spam_picture
        except Exception as e:
            self.status=str(traceback.format_exc())

    def to_json(self):
        for bot in self.list_user_bot:
            print(bot.to_json())
        print(self.target_index)
        print(self.list_target)
        print(self.list_proxy)
        print(self.status)
        print(self.spam_message)
        print(self.spam_picture)


if __name__ == "__main__":
    # username = click.prompt("Enter the number", type=str, default="anvien01111995@gmail.com")
    # password = click.prompt("Enter the number", type=str, default="To01111995")

    username = "lane287279067"
    password =  "To01111995"
    t = TwitterBot(username, password)
    t.signIn()

