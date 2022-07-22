#!/usr/bin/python

import sys

import buddy_menu

import buddy_globals as gl

def main(argv):
    buddy_menu.main_loop()


if __name__ == "__main__":
    gl.load_configuration()
    main(sys.argv[1:])
