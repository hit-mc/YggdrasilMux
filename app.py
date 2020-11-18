import json
import logging
import time

from flask import Flask, Response
from flask import request as req

from core.mux import MuxServer

# from werkzeug.serving import WSGIRequestHandler

# logging.basicConfig(filename='ym.log', filemode='a', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logging.info('YggdrasilMux is starting ...')
logging.debug('DEBUG logging is enabled.')

VERSION = "1.0-dev"
app = Flask(__name__)
mux = MuxServer([
    'https://sessionserver.mojang.com',
    'https://littleskin.cn/api/yggdrasil/sessionserver'
])


@app.route('/', methods=['GET'])
def root():
    logging.info('Root is called.')
    return {
        'mux_server': VERSION,
        'time': time.time()
    }


@app.route('/join', methods=['POST'])
def join():
    print(f'join: {req.form}')


@app.route('/sessionserver/session/minecraft/hasJoined', methods=['GET'])
def hasJoined():
    logging.debug('hasJoined is called.')
    # print(f'Received requests :{args}')
    json_str, status_code = mux.hasJoined(req.args)
    j = json.loads(json_str)
    print(f'Response: {json_str}, {status_code}')
    # return j, status_code
    return Response(json.dumps(j, indent=4), status=status_code, mimetype='application/json; charset=utf8')


# TODO: Implement `hasJoined` API

if __name__ == '__main__':
    # WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run()
