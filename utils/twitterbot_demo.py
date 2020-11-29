from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import click
import traceback
from global_assets.common import get_random_string
import datetime
from selenium.webdriver.common.proxy import Proxy, ProxyType



def init_driver_ubuntu():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def init_driver_proxy():
    chrome_options = Options()
    # proxy = Proxy()
    # proxy.proxyType = ProxyType.MANUAL
    # proxy.autodetect = True
    # proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = "65.62.63.64:9000"
    PROXY="157.65.25.144:3128"
    chrome_options.add_argument('--proxy-server=%s' % PROXY)

    print("XXXX")
    # chrome_options.add_argument("ignore-certificate-errors")



    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path="C:/Users/Lam/Documents/Selenium/chromedriver_win32/chromedriver.exe")
    # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Users/etoxlam/Documents/python_project/chromedriver.exe")
    return driver


class TwitterBot():
    def __init__(self, username, password):
        try:
            self.browser = None
            self.username = username
            self.password = password
            self.status = 'init'
            self.number_post = 0
            self.time_block = 0
            self.start_block = None
        except Exception as e:
            self.status = str(traceback.format_exc())

    def signIn(self):
        self.browser = init_driver_proxy()
        self.browser.get("https://www.google.com/")

        self.browser.get("https://www.twitter.com/login")
        time.sleep(5)
        usernameInput = self.browser.find_element_by_name("session[username_or_email]")
        passwordInput = self.browser.find_element_by_name("session[password]")
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)

        photo_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/input'
        self.browser.find_element_by_xpath(photo_xpath)
        self.status = 'OK'



    def check_block(self):
        if self.status != 'LOGIN_FAILED':
            try:
                self.status = 'CHECK BLOCK'
                self.browser.get("https://www.twitter.com/home")
                time.sleep(1)

                tweet = self.browser.find_element_by_xpath('''//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div
                                                              /div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div
                                                              /div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
                                                              /div/div/div''')
                tweet.send_keys(str("HELLO WORLD") + '\n' + str(get_random_string(8)))
                tweet.send_keys(Keys.COMMAND, Keys.ENTER)
                submit = self.browser.find_element_by_xpath(
                    '''//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]''')
                submit.send_keys(Keys.ENTER)
                try:
                    time.sleep(1)
                    alert_message = self.browser.find_element_by_xpath(
                        '''//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div''')
                    if 'Something went wrong' in alert_message.text:
                        self.status = 'BLOCKING'
                        if self.start_block is None:
                            self.start_block = datetime.datetime.now()
                            self.time_block = 0
                        self.time_block = (datetime.datetime.now() - self.start_block).total_seconds()
                    else:
                        self.status = 'OK'
                        self.start_block = None
                        self.time_block = 0
                except:
                    self.status = 'OK'
                    self.start_block = None
                    self.time_block = 0
            except Exception as e:
                self.status = str("BLOCKING")
                self.time_block = (datetime.datetime.now() - self.start_block).total_seconds()

    def TweetSomething(self, message, list_mention, image, list_tags):
        number_tag_and_mention=len(list_mention)+len(list_tags)
        for target in list_mention:
            message = message + ' @' + target + ' '

        message = message + '\n' + str(get_random_string(8))
        if self.status != 'LOGIN_FAILED':
            try:
                self.status = 'twitt'
                self.browser.get("https://www.twitter.com/home")
                time.sleep(1)

                if image is not None:
                    photo_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/input'

                    photo_element = self.browser.find_element_by_xpath(photo_xpath)
                    self.browser.execute_script("arguments[0].style.display = 'block';", photo_element)
                    photo_element.send_keys(image)
                    time.sleep(0.1)
                    if len(list_tags)>3:
                        image_tag_path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[2]/div[2]/a[1]/span'

                        tag_element = self.browser.find_element_by_xpath(image_tag_path)
                        tag_element.click()
                        time.sleep(0.05)
                        for name in list_tags:
                            try:
                                search_input = self.browser.find_element_by_xpath(
                                    '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[1]/div/div/div[2]/input')
                                search_input.send_keys('@' + str(name))
                                time.sleep(2)
                                people = self.browser.find_element_by_xpath(
                                    '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[2]/div/div[2]/div/li/div/div[2]/div/div/div/div[2]/div/span')
                                people.click()
                                time.sleep(2)
                            except:
                                number_tag_and_mention=number_tag_and_mention-1
                                try:
                                    search_input = self.browser.find_element_by_xpath(
                                        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[1]/div/div/div[2]/input')
                                    search_input.clear()
                                except:
                                    print("error")
                        done = self.browser.find_element_by_xpath(
                            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[3]/div/div/div/span/span')
                        done.click()
                        time.sleep(0.05)
                if message is not None:
                    tweet = self.browser.find_element_by_xpath('''//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div
                                                                  /div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div
                                                                  /div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
                                                                  /div/div/div''')
                    tweet.send_keys(str(message))
                    tweet.send_keys(Keys.COMMAND, Keys.ENTER)
                submit = self.browser.find_element_by_xpath(
                    '''//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]''')
                submit.send_keys(Keys.ENTER)

                try:
                    time.sleep(1)
                    alert_message = self.browser.find_element_by_xpath(
                        '''//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div''')
                    if 'Something went wrong' in alert_message.text:
                        self.status = 'BLOCKING'
                        if self.start_block is None:
                            self.start_block = datetime.datetime.now()
                            self.time_block = 0
                        self.time_block = (datetime.datetime.now() - self.start_block).total_seconds()
                    else:
                        self.number_post = self.number_post + 1
                        self.status = 'OK'
                except:
                    self.number_post = self.number_post + 1
                    self.status = 'OK'
            except Exception as e:
                self.status = 'BLOCKING'
                return 0
        return number_tag_and_mention
    def close(self):
        self.browser.close()

    def to_json(self):
        return {'username': self.username,
                'password': self.password, 'status': self.status, 'number_post': self.number_post,
                'time_block': self.time_block
                }


import os.path

if __name__ == "__main__":
    # username = click.prompt("Enter the number", type=str, default="anvien01111995@gmail.com")
    # password = click.prompt("Enter the number", type=str, default="To01111995")

    username = "lane287279067"
    password = "To01111995"
    list_target = ['ahmedbader1989rest_id', 'akhil_prabha', 'xo_generation']
    t = TwitterBot(username, password)
    t.signIn()

    t.TweetSomething('hello', list_target,'C:/Users/Lam/Pictures/BnS/032.jpg',list_target)

    # for i in range(1,2):
    #     time.sleep(1)
    #     t.TweetSomething( 'hello  ' + str(get_random_string(8)),None)
    #     while t.status=='BLOCKING':
    #         t.check_block()
    #         if t.status=='BLOCKING':
    #             time.sleep(60)
    #         print(t.to_json())
    #     print(t.to_json())
    # for i in range(1,2):
    #     time.sleep(1)
    #     t.TweetSomething( 'hello  ',None)
    #     while t.status=='BLOCKING':
    #         t.check_block()
    #         if t.status=='BLOCKING':
    #             time.sleep(60)
    #         print(t.to_json())
    #     print(t.to_json())
    # t.close()
    # if os.path.isfile('C:/Users/Lam/Documents/TOVANLAM_MMO/Twitter_auto_tweet/test/test-pic.jpg'):
    #     print("File exist")
    # else:
    #     print("File not exist")
