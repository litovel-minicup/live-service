#!/usr/bin/env python

from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line, define, options

from minicup_livestream.app import Application

define("port", default=8888, help="run on the given port", type=int)


def main():
    autoreload.start()

    parse_command_line()
    app = Application()
    app.listen(options.port)

    IOLoop.current().start()


if __name__ == "__main__":
    main()
