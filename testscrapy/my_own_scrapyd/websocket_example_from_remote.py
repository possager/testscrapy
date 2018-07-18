#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/18 17:27
# @Author  : LiangLiang
# @Site    : 
# @File    : websocket_example_from_remote.py
# @Software: PyCharm


import twisted
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
import hashlib
from base64 import b64encode
import time


class Echo(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write(
            b"Welcome! There are currently %d open connections.\n" %
            (self.factory.numProtocols,))
    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):
        self.transport.write(data)


class QOTD(Protocol):


    def connectionMade(self):
        print("a connection has been built")
        self.handshaken = False
        self.buffer = ""
        self.GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


    def dataReceived(self, data):
        headers = {}

        def set_bit(int_type, offset):
            return int_type | (1 << offset)

        def pack(data):
            """pack bytes for sending to client"""
            frame_head = bytearray(2)
            # set final fragment
            frame_head[0] = set_bit(frame_head[0], 7)
            # set opcode 1 = text
            frame_head[0] = set_bit(frame_head[0], 0)
            # payload length
            assert len(data) < 126, "haven't implemented that yet"
            frame_head[1] = len(data)
            # add data
            frame = frame_head + data.encode('utf-8')
            return frame

        def parse_recv_data(msg):
            en_bytes = b''
            cn_bytes = []
            if len(msg) < 6:
                return ''
            v = msg[1] & 0x7f
            if v == 0x7e:
                p = 4
            elif v == 0x7f:
                p = 10
            else:
                p = 2
            mask = msg[p:p + 4]
            data = msg[p + 4:]

            for k, v in enumerate(data):
                nv = chr(v ^ mask[k % 4])
                nv_bytes = nv.encode()
                nv_len = len(nv_bytes)
                if nv_len == 1:
                    en_bytes += nv_bytes
                else:
                    en_bytes += b'%s'
                    cn_bytes.append(ord(nv_bytes.decode()))
            if len(cn_bytes) > 2:
                # 字节数组转汉字
                cn_str = ''
                clen = len(cn_bytes)
                count = int(clen / 3)
                for x in range(0, count):
                    i = x * 3
                    b = bytes([cn_bytes[i], cn_bytes[i + 1], cn_bytes[i + 2]])
                    cn_str += b.decode()
                new = en_bytes.replace(b'%s%s%s', b'%s')
                new = new.decode()
                res = (new % tuple(list(cn_str)))
            else:
                res = en_bytes.decode()
            return res

        if self.handshaken == False:
                # print('Start Handshaken with {}!'.format(self.remote))
                self.buffer += bytes.decode(data)
                if self.buffer.find('\r\n\r\n') != -1:
                    header, data = self.buffer.split('\r\n\r\n', 1)
                    for line in header.split("\r\n")[1:]:
                        key, value = line.split(": ", 1)
                        headers[key] = value

                    headers["Location"] = ""
                    key = headers['Sec-WebSocket-Key']
                    token = b64encode(hashlib.sha1(str.encode(str(key + self.GUID))).digest())

                    handshake = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: " + bytes.decode(
                        token) + "\r\nWebSocket-Origin: " + str(headers["Origin"]) + "\r\nWebSocket-Location: " + str(
                        headers["Location"]) + "\r\n\r\n"

                    self.transport.write(handshake.encode("utf-8"))
                    self.handshaken = True
                    return
                    # print('Handshaken with {} success!'.format(self.remote))

        data_raw = parse_recv_data(data)

        count1 =0
        while count1 < 10:
            time.sleep(0.5)
            self.transport.write(pack("hello"))
            count1 += 1




    def connectionLost(self, reason=None):
        print("closed a connection")



class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()

class EchoFactory(Factory):
    def buildProtocol(self, addr):
        return Echo(self)


endpoint = TCP4ServerEndpoint(reactor, 9998)
endpoint1 = TCP4ServerEndpoint(reactor, 9999)
endpoint.listen(QOTDFactory())
endpoint1.listen(EchoFactory())
reactor.run()