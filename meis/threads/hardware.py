#!/usr/bin/python
# coding=utf-8

from threading import Thread
import RPi.GPIO
import json
import Queue
from meis.misc.hardware import HardwareOutput, HTTPHardwareRequest, HTTPHardwareResponse

__author__ = 'Matti Borchers'


class HardwareThread(Thread):
    def __init__(self, konfig, input_queue, flask_response_queue):
        Thread.__init__(self)
        self._hardware = []

        self._input_queue = input_queue
        self._output_queue = flask_response_queue

        RPi.GPIO.setmode(RPi.GPIO.BOARD)

        for hardware in konfig.hardware_list:
            output = HardwareOutput(id=hardware['id'],
                                    name=hardware['name'],
                                    channel=hardware['pin'],
                                    trigger_event=hardware['trigger_event'],
                                    trigger_duration=hardware['trigger_duration'],
                                    manual=hardware['manual'],
                                    inverted=hardware['inverted'])
            self._hardware.append(output)

        self._running = True

    def terminate(self):
        self._running = False

    def _get_channel_status(self, channel_id):
        for output in self._hardware:
            if output.id == channel_id:
                return output.statusdict
        return None

    def _is_valid_channel(self, channel_id):
        for output in self._hardware:
            if output.id == channel_id:
                return True
        return False

    def _get_output(self, channel_id):
        for output in self._hardware:
            if output.id == channel_id:
                return output
        return None

    def run(self):
        while self._running:

            try:
                queue_item = self._input_queue.get(True, 1)
            except Queue.Empty:
                continue

            if isinstance(queue_item, HTTPHardwareRequest):
                http_request = queue_item

                if http_request.method == 'GET':
                    # Request for status information
                    if http_request.channel != HTTPHardwareRequest.ALL_CHANNEL:
                        channel_status = self._get_channel_status(http_request.channel)
                        if channel_status is not None:
                            http_response = HTTPHardwareResponse(200, channel_status)
                        else:
                            http_response = HTTPHardwareResponse(404, None)
                    else:
                        all_channel_status = []
                        for output in self._hardware:
                            all_channel_status.append(output.statusdict)
                        http_response = HTTPHardwareResponse(200, all_channel_status)

                    self._output_queue.put(http_response)

                elif http_request.method == 'POST':
                    # Request to change a state
                    output = self._get_output(http_request.channel)
                    if output is not None:

                        output.set_state(http_request.state)
                        channel_status = self._get_channel_status(http_request.channel)
                        http_response = HTTPHardwareResponse(200, channel_status)
                    else:
                        http_response = HTTPHardwareResponse(404, None)

                    self._output_queue.put(http_response)

        RPi.GPIO.cleanup()


class HardwareKonfig:
    def __init__(self, konfigfilename):
        self._konfig_json = None

        with open(konfigfilename) as konfig_file:
            self._konfig_json = json.load(konfig_file)

    @property
    def hardware_list(self):
        return self._konfig_json['hardware']
