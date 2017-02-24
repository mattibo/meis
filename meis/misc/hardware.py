#!/usr/bin/python
# coding=utf-8
import RPi.GPIO

__author__ = 'Matti Borchers'


class HardwareOutput:
    def __init__(self, id, name, channel, trigger_event, trigger_duration,
                 manual, inverted):
        self._id = id
        self._name = name
        self._channel = channel
        self._trigger_event = trigger_event
        self._trigger_duration = trigger_duration
        self._manual = manual
        self._inverted = inverted
        self._state = False
        RPi.GPIO.setup(self._channel, RPi.GPIO.OUT)
        self.off()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        if state:
            self.on()
        else:
            self.off()

    @property
    def channel(self):
        return self._channel

    @property
    def trigger_event(self):
        return self._trigger_event

    @property
    def trigger_duration(self):
        return self._trigger_duration

    @property
    def manual(self):
        return self._manual

    @property
    def inverted(self):
        return self._inverted

    def on(self):
        if self._inverted:
            RPi.GPIO.output(self._channel, False)
        else:
            RPi.GPIO.output(self._channel, True)
        self._state = True

    def off(self):
        if self._inverted:
            RPi.GPIO.output(self._channel, True)
        else:
            RPi.GPIO.output(self._channel, False)
        self._state = False

    @property
    def statusdict(self):
        status_dict = {'id': self._id, 'name': self._name, 'state': self._state}
        return status_dict


class HTTPHardwareRequest:
    ALL_CHANNEL = 0

    def __init__(self, method, channel, state=None):
        self._method = method
        self._channel = channel
        self._state = state

    @property
    def method(self):
        return self._method

    @property
    def channel(self):
        return self._channel

    @property
    def state(self):
        return self._state


class HTTPHardwareResponse:
    def __init__(self, http_status, hardware_status):
        self._httpstatus = http_status
        self._hardwarestatus = hardware_status

    @property
    def httpstatus(self):
        return self._httpstatus

    @property
    def hardwarestatus(self):
        return self._hardwarestatus
