# SETUP SELENIUM
1. Download driver for Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
2. Put and replace "C:/Selenium/chromedriver_win32/chromedriver.exe"
3. Setup environment
## SETUP With conda
```bash
sudo su 
conda create -n twitter  python=3.8
conda activate twitter
conda  install  -y -c anaconda numpy
conda install   -y -c anaconda flask
conda install  -y  -c conda-forge flask-restplus
conda install   -y -c conda-forge flask-jsonpify
pip install selenium
pip install names==0.1
pip install pandas
pip install Werkzeug==0.16.1

git clone https://github.com/lamtov/api_twitter.git
cd api_twitter/
python app.py

```
##  RUN:
```bash
http://localhost:5009/index
```



