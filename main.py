#!/usr/bin/env python

from twisted.internet import reactor
from lib.bot import Proto4Bot

def main():
    host = raw_input('Host: ')
    while True:
        try:
            port = int(raw_input('Port: '))
            break
        except TypeError:
            print 'Port must be an integer!'
    reactor.connectTCP(host, port, Proto4Bot())
    reactor.run()

if __name__ == '__main__':
    main()
