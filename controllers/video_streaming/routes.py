from  flask import Flask, render_template, Response
from flask import session
from flask_socketio import emit, join_room, leave_room
from jinja2 import TemplateNotFound
import config
import  os, time,cv2, sys
from flask_restplus import Api, Resource,Namespace
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from .assets import VideoCamera
from . import  mod
import  base64
my_video1 = VideoCamera('static/video/video1.mp4')
frame1 = my_video1.get_frame()
# my_video2 = VideoCamera('static/video/video1.mp4')
frame2 = frame1
play = False
face_detector=False
speed = .300
room_id =1
import socketio


@mod.route('/test_video')
def index():
    return render_template('stream_video.html')

# Using python generator for update image (main core of streaming and broadcast)
def gen(video_id):
    while True:
        time.sleep(speed)
        if video_id == 1:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n\r\n')
# Main_ROle for select video  to load list image by image
@mod.route('/video_feed/<int:video_id>')
def video_feed(video_id):
    return Response(gen(video_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
def gen_test(video_id):
    while True:
        time.sleep(speed)
        if video_id == 1:
            yield (frame1)
        else:
            yield (frame2)
@mod.route('/frame_feed/<int:video_id>')
def frame_feed(video_id):
    return Response(gen_test(video_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



# For Play Pause Button
@mod.route('/play_pause', methods=['POST'])
def play_pause():
    global play
    play = not play

    print('connected')
    return {"ok": "done"}


# For Speed Up Button
@mod.route('/speed_up', methods=['POST'])
def speed_up():
    global speed
    speed = speed / 2
    return {"ok": "done"}

# For Speed Down Button
@mod.route('/speed_down', methods=['POST'])
def speed_down():
    global speed
    speed = speed * 2
    return {"ok": "done"}

# For Reload Button
@mod.route('/reload', methods=['POST'])
def reload():
    my_video1.reload()
    my_video2.reload()
    return {"ok": "done"}

@mod.route('/on_of_face', methods=['POST'])
def on_of_face():
    global face_detector
    face_detector = not face_detector
    return {"ok": "done"}

# I create an easy demo of upload image for broadcast using load next image in video
# @mod.route('/test_update_camera', methods=['GET','POST'])

# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 5009       # The port used by the server
# from socketIO_client import SocketIO, BaseNamespace
# socket = SocketIO(HOST, PORT)
# chat = socket.define(BaseNamespace, '/thermoai')
def test_socket(chat):
    try:
        frame_demo = my_video1.get_frame()
        image_frame = "data:image/jpeg;base64," + str(base64.b64encode(frame_demo))
        chat.emit('image_frame', {'id': 1, 'image_frame': image_frame})
        # socket.disconnect()
    except:
        e = sys.exc_info()[0]
        print(e)



# def update_camera_image():
#     global frame1
#     global frame2
#     global my_video1
#     global my_video2
#     time.sleep(20)
#     socket = SocketIO(HOST, PORT)
#     chat = socket.define(BaseNamespace, '/thermoai')
#     while True:
#         while play:
#             time.sleep(speed)
#             if face_detector:
#                 frame1 = my_video1.get_frame_and_face_detector()
#                 image_frame ="data:image/jpeg;base64," + str(base64.b64encode(frame1))
#                 chat.emit('image_frame', {'id': 1, 'image_frame': image_frame})
#             else:
#                 frame1 = my_video1.get_frame()
#                 image_frame = "data:image/jpeg;base64," + str(base64.b64encode(frame1))
#                 chat.emit('image_frame', {'id': 1, 'image_frame': image_frame})
    # return {"ok": "done"}
