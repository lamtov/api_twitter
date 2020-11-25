from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import click
import traceback

def init_driver_ubuntu():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver
def init_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Users/Lam/Documents/Selenium/chromedriver_win32/chromedriver.exe")
    return driver

class TwitterBot():
    def __init__(self, username, password):
        try:
            self.browser = init_driver()
            self.username = username
            self.password = password
            self.status='init'
            self.number_post=0
            self.time_block=0
        except Exception as e:
            self.status=str(traceback.format_exc())

    def signIn(self):
        try:
            self.browser.get("https://www.twitter.com/login")
            time.sleep(5)
            usernameInput = self.browser.find_element_by_name("session[username_or_email]")
            passwordInput = self.browser.find_element_by_name("session[password]")
            usernameInput.send_keys(self.username)
            passwordInput.send_keys(self.password)
            passwordInput.send_keys(Keys.ENTER)
            print("__________ FINISHED SIGNIN")
            time.sleep(2)

            photo_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/input'
            photo_element = self.browser.find_element_by_xpath(photo_xpath)
            print(type(photo_element))
            self.status = 'OK'
        except Exception as e:
            self.status = str('LOGIN_FAILED')
    def check_block(self):
        if self.status != 'LOGIN_FAILED':
            try:
                self.status='CHECK BLOCK'
                self.browser.get("https://www.twitter.com/home")
                time.sleep(1)


                tweet = self.browser.find_element_by_xpath('''//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div
                                                              /div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div
                                                              /div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
                                                              /div/div/div''')
                tweet.send_keys(str("HELLO WORLD"))
                tweet.send_keys(Keys.COMMAND, Keys.ENTER)
                submit = self.browser.find_element_by_xpath(
                    '''//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]''')
                submit.send_keys(Keys.ENTER)

                print("__________ FINISHED TWEET CHECK IN https://twitter.com/home")
                try:
                    time.sleep(1)
                    alert_message = self.browser.find_element_by_xpath(
                        '''//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div''')
                    if 'Something went wrong' in alert_message.text:
                        self.status = 'BLOCKING'
                        print("OK")
                except:
                    self.status = 'OK'
            except Exception as e:
                self.status = str("BLOCKING")
                self.time_block=self.time_block+60
                # time.sleep(60)
    def TweetSomething(self, message,image):
        if self.status != 'LOGIN_FAILED':
            try:
                self.status='twitt'
                self.browser.get("https://www.twitter.com/home")
                time.sleep(1)

                if image is not None:
                    photo_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/input'

                    photo_element = self.browser.find_element_by_xpath(photo_xpath)
                    photo_element.send_keys(image)

                time.sleep(1)

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

                print("__________ FINISHED TWEET CHECK IN https://twitter.com/home")
                self.number_post=self.number_post+1
                self.time_block=0
                self.status='OK'
                try:
                    time.sleep(1)
                    alert_message=self.browser.find_element_by_xpath('''//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div''')
                    if 'Something went wrong' in alert_message.text:
                        self.status='BLOCKING'
                        print("???")
                except:
                    self.status='OK'
            except Exception as e:
                self.status = 'BLOCKING'

    def to_json(self):
        return {'username':self.username,
            'password' :self.password,'status': self.status, 'number_post':self.number_post,
                'time_block':self.time_block
                }
import os.path


if __name__ == "__main__":
    # username = click.prompt("Enter the number", type=str, default="anvien01111995@gmail.com")
    # password = click.prompt("Enter the number", type=str, default="To01111995")

    username = "lane287279067"
    password =  "To01111995"
    t = TwitterBot(username, password)
    t.signIn()

    for i in range(1,1000):
        time.sleep(1)
        t.TweetSomething( 'hello  ',None)
        while t.status=='BLOCKING':
            t.check_block()
            if t.status=='BLOCKING':
                time.sleep(60)
            print(t.to_json())
        print(t.to_json())
    # if os.path.isfile('C:/Users/Lam/Documents/TOVANLAM_MMO/Twitter_auto_tweet/test/test-pic.jpg'):
    #     print("File exist")
    # else:
    #     print("File not exist")