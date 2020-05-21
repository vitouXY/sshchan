#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Configuration class holds settings loaded from a JSON file (or uses
defaults). Settings contain important paths that are used throughout
the program, and can be modified to contain other data easily.

Copyright (c) 2015
makos <https://github.com/makos>, chibi <http://neetco.de/chibi>
under GNU GPL v3, see LICENSE for details
"""

import os
import sys
import json
import logging

from pdata import getrandname

logging.basicConfig(
    filename="log",
    format="[%(lineno)d]%(asctime)s:%(levelname)s:%(message)s",
    level=logging.DEBUG)


class Colors():
    """Terminal escape codes for colored output."""

    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    BLACK = '\033[0m'

    # Bold (bright) variants of the same colors above.
    bRED = '\033[1;31m'
    bYELLOW = '\033[1;33m'
    bGREEN = '\033[1;32m'
    bBLUE = '\033[1;34m'
    bPURPLE = '\033[1;35m'
    bBLACK = '\033[1m'


class Config():
    """This class holds config data, paths to important files etc."""

    # XXX REMEMBER to put every new config option in here. XXX #
    defaults = {"rootdir": "/srv/chan",
                "boardlist_path": "/srv/chan/boardlist",
                "postnums_path": "/srv/chan/postnums",
                "motd_path": "/srv/chan/motd",
                "version": "0.0",
                "name": "toLang(es_ES).beta",
                "prompt": "@Chan",
                "port_ssh": "22",
                "display_legacy": "True"}

    def __init__(self, cfg_path=""):
        # Find config file.

        self.path = self.look_for_config(
            cfg_path,
            os.getcwd() + "/atchan.conf",
            os.getenv('HOME', default="~") + "/atchan.conf",
            "/etc/atchan.conf")

        self.root = self.get_cfg_opt("rootdir", "/srv/chan", fatal=True)
        self.boardlist_path = self.get_cfg_opt(
            "boardlist_path", self.root + "/boardlist")
        self.postnums_path = self.get_cfg_opt(
            "postnums_path", self.root + "/postnums")
        self.version = self.get_cfg_opt("version", "0.0")
        self.motd = self.get_cfg_opt("motd_path", "/etc/motd")
        self.port_ssh = self.get_cfg_opt("port_ssh", "22")
        self.server_name = self.get_cfg_opt("name", "toLang(es_Es).beta")
        self.username = os.getenv("USERNAME", default=getrandname()) #default="anonymous")
        self.max_boards = 10  # How many boards can be displayed in top bar.
        self.display_legacy = self.get_cfg_opt("display_legacy", "True")
        self.prompt = self.get_cfg_opt("prompt", "@Chan")
        # self.admin = settings["admin"]
        # self.salt = settings["salt"]
        # self.passwd = settings["password"]

        # Max threads on page.
        self.max_threads = 14
        # Terminal size.
        self.tty_cols = os.get_terminal_size()[0]
        self.tty_lines = os.get_terminal_size()[1]
        # Used for laprint() from Display.
        self.lines_printed = 0

    def look_for_config(self, *args):
        '''Looks for the config in the paths specified in *args until
        one that works is found.'''
        argv = list(args)
        while len(argv) != 0:
            if os.path.exists(argv[0]) == True:
                return str(argv[0])
            else:
                argv.pop(0)
                continue

        # If no config file coud be found
        print(Colors.bRED + '[FATAL] No se pudo encontrar el archivo de configuracion.' +
              Colors.BLACK) # [FATAL] Config file could not be found.
        sys.exit(1)

    def get_cfg_opt(self, opt_name, default, fatal=False):
        """Reads a value from the config file.
        opt_name is the key of the config value.
        default is the default value if reading fails.
        fatal, if True, means that a failure to read the option must
        terminate sshchan.
        """
        config = self.load()
        try:
            answer = config[opt_name]
            return answer
        except KeyError:
            if fatal:
                print(
                    Colors.bRED + "[FATAL] La opcion de configuracion \'{0}\' no se pudo \
                            encontrar en el archivo \'{1}\'.".format
                    (opt_name, self.path) + Colors.BLACK) # [FATAL] Config option \++\ could not be found in file 
                sys.exit(1)
            else:
                logging.warning(
                    "Could not find the value for option {0} in config."
                    .format(opt_name))
                return default

    def set_cfg_opt(self, opt_name, new_value):
        """Set configuration option opt_name to new_value."""
        config = self.load()
        if opt_name not in self.defaults.keys():
            logging.error(
                "\"{0}\" is not a configuration option.".format(opt_name))
            return False
        config[opt_name] = new_value
        self.save(config)
        return True

    def load(self):
        """Load a JSON configuration file, or return default values."""
        try:
            with open(self.path, 'r') as c:
                config = json.load(c)
            # logging.info("Loaded JSON config file.")
            return config
        except FileNotFoundError:
            logging.warning("Config file at %s not found, returning defaults.",
                            self.path)
            return Config.defaults

    def save(self, values):
        """Save new or udpated settings to a JSON file."""
        with open(self.path, 'w') as c:
            json.dump(values, c, indent=4)
        logging.info("Dumped new settings into %s.", self.path)
        return True

    def get_boardlist(self):
        """Return the boardlist as a Python dictionary."""
        with open(self.boardlist_path, 'r') as b:
            buf = json.load(b)
        return buf

    def set_boardlist(self, values):
        """Update/create the boardlist with values.

        Boardlist is a standard Python dictionary in the form of
        {"boardname": "description", ...}
        where boardname should be just the name without any slashes
        (but they are not forbidden).
        """
        with open(self.boardlist_path, 'w') as b:
            json.dump(values, b, indent=4)
        logging.info("Updated boardlist file.")
        return True

    def get_postnums(self):
        """Return the postnums file as a Python dictionary."""
        with open(self.postnums_path, 'r') as p:
            buf = json.load(p)
        return buf

    def set_postnums(self, values):
        """Update/create the postnums for board name with value."""
        with open(self.postnums_path, 'w') as p:
            json.dump(values, p, indent=4)
        logging.info("Updated postnums file.")
        return True
