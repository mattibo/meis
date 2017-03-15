#!/usr/bin/python
# coding=utf-8

import json
import locale
import os
import sys

__author__ = 'Matti Borchers'

enc = locale.getpreferredencoding()


def console_print(st=u"", f=sys.stdout, linebreak=True):
    """Write st to f with or without linebreak."""
    f.write(st.encode(enc))
    if linebreak:
        f.write(os.linesep)


def console_flush(f=sys.stdout):
    """Flush f."""
    f.flush()


class KonfigDecoder:

    _filename = u""
    _jsondata = None

    def __init__(self, filename):
        self._filename = filename
        with open(self._filename) as f:
            self._jsondata = json.load(f)
    #
    # @property
    # def konfig_object(self):
    #     return self._jsondata
    #
    # @property
    # def database(self):
    #     return self._jsondata[DATABASE]
    #
    # @property
    # def wehrname(self):
    #     return self._jsondata[WEHR]
    #
    # @property
    # def mail_object(self):
    #     return self._jsondata[MAIL]
    #
    # @property
    # def mailbody(self):
    #     return self.mail_object[MAIL_BODY]
    #
    # @property
    # def mailfromname(self):
    #     return self.mail_object[MAIL_FROM_NAME]
    #
    # @property
    # def mailfrom(self):
    #     return self.mail_object[MAIL_FROM]
    #
    # @property
    # def mailuser(self):
    #     return self.mail_object[MAIL_USER]
    #
    # @property
    # def mailpw(self):
    #     return self.mail_object[MAIL_PW]
    #
    # @property
    # def mailto(self):
    #     return self.mail_object[MAIL_TO]
    #
    # @property
    # def mailserver(self):
    #     return self.mail_object[MAIL_SERVER]
    #
    # @property
    # def mailcc(self):
    #     return self.mail_object[MAIL_CC]
    #
    # @property
    # def mailport(self):
    #     return self.mail_object[MAIL_PORT]
    #
    # @property
    # def mailsubject(self):
    #     return self.mail_object[MAIL_SUBJECT]
    #
    # @property
    # def hardware_list(self):
    #     return self._jsondata[HARDWARE]
    #
    # @property
    # def serialport(self):
    #     return self._jsondata[SERIALPORT]

    def __getattr__(self, name):
        try:
            return self._jsondata[name]
        except KeyError:
            return None

    def reload(self):
        """Lädt die Konfiguration erneut aus der Konfigurations-Datei ein."""
        # TODO: Konfig refresh implementieren
        pass

konfig = KonfigDecoder(u"konfig.json")


def is_konfig_valid():
    """Return if the configuration File is valid."""
    if not konfig.serial:
        return False
    if not konfig.wehr:
        return False
    if not konfig.wehr[u"id"]:
        return False
    if not konfig.wehr[u"name"]:
        return False
    return True
