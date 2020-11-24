import socket
# HOST = '127.0.0.1'  # The server's hostname or IP address
HOST = '35.213.153.96'
PORT = 5009       # The port used by the server
from socketIO_client import SocketIO, BaseNamespace
socket = SocketIO(HOST, PORT)
chat = socket.define(BaseNamespace, '/monitor')
# chat.emit('make_connect', 'hello openchat my name is Anderson')
chat.emit('thermoai_view', '{"id":5 }')
# chat = socket.define(BaseNamespace, '/thermoai')
# chat.emit('image_frame', '{"id": 1, "image_frame": 2313123123132}')