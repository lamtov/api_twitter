import socket
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5009       # The port used by the server
from socketIO_client import SocketIO, BaseNamespace
socket = SocketIO(HOST, PORT)
chat = socket.define(BaseNamespace, '/monitor')
chat.emit('make_connect', 'hello openchat my name is Anderson')
chat.emit('image_frame', {'id':1 , 'image_frame': 21312321321})
def on_aaa_response(*args):
    print('on_aaa_response', args)
chat.on('thermoai_stream',on_aaa_response)
socket.wait()