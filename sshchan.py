#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/python3
#qpy:console
"""
Main file of sshchan, it ties up other files together.
User interacts with the chan through the use of a commandline.
Any user can create new threads, reply to other posts and freely browse
the boards. Only admins can add boards.

Copyright (c) 2015
makos <https://github.com/makos>, chibi <http://neetco.de/chibi>
under GNU GPL v2, see LICENSE for details
"""
# TODO:
# Find config file in home dir or CWD
import logging
import sys
import os
#import urwid
import re
# sshchan imports
# import admin
import config
from boards import Board
from chan_mark import Marker
#import display
from display_legacy import DisplayLegacy
from dl_cmdline import DisplayLegacyCmdline

import signal
def keyboardInterruptHandler(signal, frame ):
    print( "KeyboardInterrupt (ID: {}) has been caught. Cleaning up..." . format(signal ))
    exit(0)
signal.signal(signal.SIGINT, keyboardInterruptHandler)

logging.basicConfig(
    filename="log",
    format="[%(lineno)d]%(asctime)s:%(levelname)s:%(message)s",
    level=logging.DEBUG)

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                cfg = config.Config(sys.argv[1])
            else:
                # Change it so it at least tries to read default path/values first.
                print("Ruta de archivo de configuracion no valida.") # Invalid configuration file path.
                cfg = config.Config()
        else:
            cfg = config.Config()
    except OSError:
        exit(0)

    board = Board(config=cfg)
    c = config.Colors() # terminal colors object
    marker = Marker()
    dl = DisplayLegacy(cfg, board, c, marker)


    import pkgutil
    mloader = pkgutil.find_loader( 'urwid' )
    mfound = mloader is not None
    if mfound == False:
        screen = DisplayLegacyCmdline(board, c, cfg, dl, marker)
        screen.run()
    else:
        # Command line legacy interface - used by default
        if cfg.display_legacy in ("True", "true"): 
            screen = DisplayLegacyCmdline(board, c, cfg, dl, marker)
            screen.run()
        # urwid GUI
        else:
            import urwid
            import display

            screen = display.Display(cfg, board)
            screen.run()

