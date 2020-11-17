from flask import Flask
from flask import request as req
import json
from core.mux import MuxServer

VERSION = "1.0"
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
    return mux.hasJoined(req.form)


# TODO: Implement `hasJoined` API

if __name__ == '__main__':
    app.run()
