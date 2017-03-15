#!/usr/bin/python
# coding=utf-8
from threading import Thread

from misc import konfig

__author__ = 'Matti Borchers'


class MailingThread(Thread):

    _server = konfig.mail[u"server"]
    _port = int(konfig.mail[u"port"])
    _user = konfig.mail[u"user"]
    _pw = konfig.mail[u"pw"]
    _from = konfig.mail[u"from"]
    _from_name = konfig.mail[u"from_name"]

    def __init__(self):
        Thread.__init__(self, name='MailingThread')

    def run(self):
        while True:
            queue