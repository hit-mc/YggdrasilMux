import logging
import time

from fastapi import FastAPI, Response

from core.mux import MuxServer

# from werkzeug.serving import WSGIRequestHandler
# logging.basicConfig(filename='ym.log', filemode='a', level=logging.DEBUG)

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s][%(asctime)s][line:%(lineno)d] %(message)s')
logging.info('YggdrasilMux is starting ...')
logging.debug('DEBUG logging is enabled.')

VERSION = "1.0-dev"
app = FastAPI()
mux = MuxServer([
    'https://sessionserver.mojang.com',
    'https://mcskin.littleservice.cn/api/yggdrasil/sessionserver'
])


@app.get('/') # methods=['GET']
async def root():
    logging.info('Root is called.')
    return {
        'mux_server': VERSION,
        'time': time.time()
    }


# @app.route('/join', methods=['POST'])
# def join():
#     logging.info(f'join was called: {req.form}')


@app.get('/sessionserver/session/minecraft/hasJoined') # methods=['GET', 'POST']
async def hasJoined(username, serverId):
    args = {"username": username, "serverId": serverId}
    logging.debug(f'hasJoined is called. args={args}')
    # print(f'Received requests :{args}')
    json_str, status_code = mux.hasJoined(args)
    # try:
    #     j = json.loads(json_str)
    #     json_str = json.dumps(j, indent=4)
    # except JSONDecodeError:
    #     logging.warning(f'Failed to decode string {json_str} as json. Use raw string instead.')

    logging.info(f'Mux make response with statcode={status_code}: {json_str}')
    # return j, status_code
    # ; charset=utf8
    return Response(json_str, status_code=status_code, media_type='application/json', headers={"Connection": "close"})


# @app.route('/api/profiles/minecraft', methods=['POST'])
# def query_profiles():
#     # data = req.data
#     logging.debug(f'profiles is called. data={data}')

    # json_str, status_code = mux.profile()

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     logging.error(f'Uncaught query path: {path}')
#     return 'You want path: %s' % path


# TODO: Implement `hasJoined` API

# if __name__ == '__main__':
#     # WSGIRequestHandler.protocol_version = "HTTP/1.1"
#     app.
