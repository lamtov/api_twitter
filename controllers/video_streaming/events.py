# from flask import session
# from flask_socketio import emit, join_room, leave_room
# from app import socketio
#
# print("AXXXX")
# @socketio.on('make_connect' ,namespace='/chat')  # global namespace
# def make_connect(message):
#     print('make connection')
#     room = session.get('room') or 1
#     join_room(room)
#     print(message)
#     # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
#
# @socketio.on('xyze' ,namespace='/chat')  # global namespace
# def xyze(message):
#     print('make connection')
#     room = session.get('room') or 1
#     join_room(room)
#     print(message)
# @socketio.on('joined', namespace='/thermoai')
# def joined(message):
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     join_room(room)
#     emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
#
#
# @socketio.on('text', namespace='/thermoai')
# def text(message):
#     """Sent by a client when the user entered a new message.
#     The message is sent to all people in the room."""
#     room = session.get('room')
#     emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)
#
#
# @socketio.on('left', namespace='/thermoai')
# def left(message):
#     """Sent by clients when they leave a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     leave_room(room)
#     emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)