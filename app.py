from flask import Flask
from flask import request as req
import json
import logging
from core.mux import MuxServer

logging.basicConfig(filename='ym.log', filemode='a', level=logging.DEBUG)
logging.info('YggdrasilMux is starting ...')

VERSION = "1.0-dev"
app = Flask(__name__)
mux = MuxServer([
    'https://sessionserver.mojang.com',
    'https://littleskin.cn/api/yggdrasil/sessionserver'
])

@app.route('/')
def root():
    return {
        'mux_server': VERSION,
    }

@app.route('/sessionserver/session/minecraft/hasJoined', methods=['GET'])
def hasJoined():
    print(f'Received requests :{req.args}')
    response = mux.hasJoined(req.args)
    print(f'Response: {response}')
    return response


# TODO: Implement `hasJoined` API

if __name__ == '__main__':
    app.run()
