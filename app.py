import logging

import uvicorn
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
    'https://littleskin.cn/api/yggdrasil/'
])
content_type = 'application/json; charset=utf-8'


@app.get('/')  # methods=['GET']
async def root():
    text, status_code = mux.get_root()
    return Response(content=text, status_code=status_code, media_type=content_type)


@app.get('/sessionserver/session/minecraft/hasJoined')  # methods=['GET', 'POST']
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
    return Response(json_str, status_code=status_code, media_type=content_type, headers={"Connection": "close"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
