#!/usr/bin/env python

from tornado.options import define

from minicup_livestream.app import main

if __name__ == "__main__":
    exit(main())
