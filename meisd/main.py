#!/usr/bin/python
# coding=utf-8

import os
import signal
import time

from misc import is_konfig_valid
from misc import console_flush
from misc import console_print
from misc import konfig

__author__ = 'Matti Borchers'


def main():
    pidfile = os.path.expanduser("~/.meis/meis.pid")

    with open(pidfile, 'w') as f:
        f.write(str(os.getpid()))

    def sigterm_handler(signo, frame):
        console_print(u"terminated!")
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == '__main__':
    if not is_konfig_valid():
        console_print(u"Konfigurationsdatei fehlerhaft!")
        raise SystemExit(1)
    main()
    while True:
        console_print("alive!")
        console_flush()
        time.sleep(10)
