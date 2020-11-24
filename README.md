# Thermo Ai Central Server
Broadcast Image, Video  with the help of Flask and Opencv
## SETUP With conda
```bash
sudo su 
conda create -n javis  python=3.8
conda activate javis
conda  install  -y -c anaconda numpy
conda install   -y -c anaconda flask
conda install  -y  -c conda-forge flask-restplus
pip install Werkzeug==0.16.1
conda install   -y -c conda-forge flask-wtf
conda install   -y -c conda-forge flask-jsonpify
conda install   -y -c conda-forge flask-socketio
conda install   -y -c conda-forge opencv
# for cloud vm only: sudo apt install libgl1-mesa-glx 
git clone https://git.javis.vn/thermal-detection/thermo-ai-central-server.git
cd thermo-ai-central-server/
python app.py

```
##  Demo:
```bash
http://35.213.153.96:5009/
```


## Start the service:
    python3 app.py
## What news: 
* I'm using app_dev.py because I have many problem with set up current library in my local environment like:
  -  YOLOv3 Problem
  - Tensorrt and CUDA
...

* I move all librarys (or some other github code we used) to the folder libs/ to make sure we never see or submit lib more than 1 times. The libs should be here for easy call, update 

* I move all models to models like: Model Persons, Model Network in Yolo_net. It make MVC look.
* I create logs. When app run it will save log in app.log and make backup log every night

* For config I create conf.py with class Config inside config folder because flask has an default app.config(ConfigObject)

### To help us code with multiple dev and multiple submit I suggest we use Blueprint like this
Each dev or each task should be a module in foolder controllers:
 * controllers: 
    * __init__.py
    * spec_network
      * templates  # list template file html, css using inside this module
      * __init__.py
      * assets.py # list python function
      * events.py # list socket like socket.on, socket.emit
      * forms.py  # list form using WTForm
      * routes.py # list route like /home, /login, /chat
    * test_api
    * thermal_app_bk
 * Like this example above we have 3 module in controllers
   * the test_api is for test and read structure
   * the thermal_app_bk is the old version of thermal app
   * the spec_network is my current task with I set all socket function inside spec_network/templates/chat_thermo_server
 * Each module now have diffent templates and diffent code in diffent file, folder
 * After create a new task, module inside controller go to the app_dev.py add 
```sh 
   register_module("test_api")
   register_module('spec_network')
```
* Or if you dont want to use/test some module, just comment.
# 
pip install eventlet