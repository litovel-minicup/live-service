#!/usr/bin/env python

from tornado.options import define

from minicup_live_service.app import main

if __name__ == "__main__":
    exit(main())
