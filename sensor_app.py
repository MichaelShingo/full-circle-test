from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
from opcua import Client;
import time

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, async_mode='eventlet') # cors_allowed_origins='*'

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Receive information from turbine
"""
def background_thread():    
    server_endpoint = 'opc.tcp://31.21.225.234:4840'
    username = 'Testcase'
    password = 'FullCircle'
    client = Client(server_endpoint)
    client.set_user(username)
    client.set_password(password)
    client.connect()
    print('client connected')
    node_id = 'ns=2;s=NACELLEM/Variables/fCPUUsage_var'
    while True:
        FCPUUsage = client.get_node(node_id)
        cpu = FCPUUsage.get_value()
        print(cpu)
        socketio.emit('updateSensorData', {'value': cpu, "date": get_current_datetime()})
        socketio.sleep(1)

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)