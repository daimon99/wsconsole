# coding: utf-8

import asyncio

import websockets
import logging
import subprocess

from websockets.compatibility import UNAUTHORIZED, OK

PIN = '123456'

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


def decode_(str_):
    """
    """
    text = str_
    charests = ('utf8', 'gbk', 'gb2312', 'big5', 'ascii',
                'shift_jis', 'euc_jp', 'euc_kr', 'iso2022_kr',
                'latin1', 'latin2', 'latin9', 'latin10', 'koi8_r',
                'cyrillic', 'utf16', 'utf32'
                )
    if isinstance(text, str):
        return text
    else:
        for i in charests:
            try:
                return text.decode(i)
            except:
                pass
        else:
            return None


async def echo(ws, path):
    try:
        async for message in ws:
            try:
                log.info('--> %s', message)
                result = subprocess.check_output(message, shell=True, timeout=10)
                await ws.send(decode_(result))
            except subprocess.CalledProcessError as e:
                await ws.send(str(e))
            except subprocess.TimeoutExpired:
                await ws.send('Timeout!')
    except websockets.ConnectionClosed:
        log.info('connection closed')


class AuthProtocol(websockets.WebSocketServerProtocol):
    @asyncio.coroutine
    def process_request(self, path, request_headers):
        if path == '/ws-console/':
            with open('client.html', 'rb') as f:
                html = f.read()
            return OK, [], html
        if path != '/ws/?pin=%s' % PIN:
            print(request_headers, request_headers['Sec-WebSocket-Protocol'])
            return UNAUTHORIZED, []
        else:
            return None


server = websockets.serve(echo, 'localhost', 5678, create_protocol=AuthProtocol)

asyncio.get_event_loop().run_until_complete(
    server
)
log.info('Server started.')

asyncio.get_event_loop().run_forever()
