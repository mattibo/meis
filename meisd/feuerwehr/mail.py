#!/usr/bin/python
# coding=utf-8

__author__ = 'Matti Borchers'


class MailObject:

    _to = []
    _cc = []
    _subject = u""
    _body = u""

    def __init__(self, to=None, cc=None, subject="", body=""):
        if to is None:
            self._to = []
        else:
            self._to = to
        if cc is None:
            self._cc = []
        else:
            self._cc = cc
        self._subject = subject
        self._body = body

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, value):
        self._to = value

    @property
    def cc(self):
        return self._cc

    @cc.setter
    def cc(self, value):
        self._cc = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value


class EinsatzMailObject:

    def __init__(self, einsatz):
        pass


class EinsatzAnalyzeObject:

    def __init__(self):
        pass
