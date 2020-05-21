#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/python3
#qpy:console
"""Admin commandline interface, accessible after succesful authentication.

Copyright (c) 2015
makos <https://github.com/makos/>, chibi <http://neetco.de/chibi>
under GNU GPL v2, see LICENSE for details
"""

import logging
import sys
import os
import config
from boards import Board
from chan_mark import Marker
import helptexts

import console
import readline
import getpass

import signal
"""
def signal_handler(sig, frame):
    # ctrl+ C_SIGINT \_SIGQUIT
    print (' Wut!? ')
    sys.exit(0)
"""
def keyboardInterruptHandler(signal, frame ):
    print( "KeyboardInterrupt (ID: {}) has been caught. Cleaning up..." . format(signal ))
    exit(0)
signal.signal(signal.SIGINT, keyboardInterruptHandler)

logging.basicConfig(
    filename="log",
    format="[%(lineno)d]%(asctime)s:%(levelname)s:%(message)s",
    level=logging.DEBUG)

def admin_help(c):
    print(helptexts.admin_helptext)

def cmdline(cfg, board, c):

    # tab version from console.py
    ctab = console.Console(c.BLUE + "@Chan/" + c.RED + "ADMIN" + c.BLUE + "> "+ c.BLACK) #(">>> ")
    ctab.autocomplete(["help", "list", "add", "rmboard", "rm", "rename", "config", "lsconfig", "exit"])
    cmd = str(ctab.console(intro="", autocomplete=True))

    # nomal version
    #cmd = str(input(c.BLUE + "@Chan/" + c.RED + "ADMIN" + c.BLUE + "> "+
    #                c.BLACK))
    cmd_argv = []
    cmd_argv = cmd.split()

    #if len(cmd_argv) < 1:
    #if cmd_argv == [] :
    if len(cmd_argv) == 0:
        return False

    elif cmd_argv[0] in ("help", "h"):
        admin_help(c)

    elif cmd_argv[0] in ("list", "ls"):
        print(board.list_boards())

    elif cmd_argv[0] == "add":
        if len(cmd_argv) > 2:
            description = ''
            board.name = cmd_argv[1]
            for word in cmd_argv[2:]:
                description += word + ' '
            board.desc = description.rstrip()
            if board.add_board():
                print(c.GREEN + "Tablero /", board.name, "/ agragado \
con exito." + c.BLACK) # Board /++/ added succesfully.
            else:
                print(c.RED + "Se ha producido un error al crear el tablero.",
                      c.BLACK) # There was an error creating the board.
        else:
            print(c.RED + "Por favor proporcione el nombre y la descripcion del tablero \
separados por espacios en blanco.", c.BLACK) # Please provide board name and description separated by whitespace.

    elif cmd_argv[0] == "rmboard":
        if len(cmd_argv) > 1:
            board.name = cmd_argv[1]
            answer = str(input("Estas seguro de que deseas eliminar el \
tablero /" + board.name + "/? (s/n): ")) # Are you sure you want to delete board /++/? (y/n):
            if answer == "s": # y
                if board.del_board():
                    print(c.GREEN + "Tablero eliminado exitosamente.", c.BLACK) # Board deleted succesfully.
                else:
                    print(c.RED + "La eliminacion del tablero fallo.", c.BLACK) # Board deletion failed.
            else:
                print(c.GREEN + "Ninguna accion tomada.", c.BLACK) # No action taken.
        else:
            print(c.RED + "Por favor, especifique el tablero que desea eliminar.",
                  c.BLACK) # Please specify the board you want to delete.

    elif cmd_argv[0] == "rm":
        if len(cmd_argv) >= 3:
            board.rm_post(cmd_argv[1], cmd_argv[2])
        else:
            print(c.RED + "No hay suficientes argumentos suministrados." + c.BLACK) # Not enough arguments supplied.

    elif cmd_argv[0] == "rename":
        if len(cmd_argv) > 2:
            name = cmd_argv[1]
            newdesc = ' '.join(cmd_argv[2:])
            if board.rename(name, newdesc):
                print(c.GREEN + "Tablero renombrado exitosamente.", c.BLACK) # Board renamed successfully.
            else:
                print(c.RED + "Error al cambiar el nombre del tablero.", c.BLACK) # Failed to rename board.
        else:
            print(
                c.RED +
                "Por favor, especifique el tablero y su nueva descripcion.",
                c.BLACK) # Please specify the board and its new description.

    elif cmd_argv[0] == "config":
        """Changes a configuration option."""
        if len(cmd_argv) >= 3:
            if cfg.set_cfg_opt(cmd_argv[1], " ".join(cmd_argv[2:])):
                print(
                    c.GREEN + "El archivo de configuracion se modifico con exito." +
                    c.BLACK) # Configuration file changed successfully.
            else:
                print(c.RED + "Error al modificar el archivo de configuracion\n\
Compruebe que la option existe primero." + c.BLACK) # Failed to change configuration file. ++ Check that the option exists first.
        else:
            print(c.RED + "Proporcione al menos dos argumentos: \
la opcion de configuracion y el valor al que desea cambiarlo." + c.BLACK) # Please provide at least two arguments: the configuration option and the value you want to change it to.

    elif cmd_argv[0] == "lsconfig":
        """List configuration options and their current values."""
        opts = sorted(cfg.defaults.keys())
        for opt in opts:
            value = cfg.get_cfg_opt(opt, c.RED + "no establecido /" + c.BLACK \
+ " por defecto: " + c.GREEN + cfg.defaults[opt] + c.BLACK) # not set /++ default: 
            print(opt.ljust(20) + value)

    elif cmd_argv[0] in ("exit","q","exit"):
        sys.exit(0)
    else:
        print(c.RED + "Comando " + cmd_argv[0] + " no encontrado." + c.BLACK) # Command ++ not found.

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            cfg = config.Config(sys.argv[1])
        else:
            print("Ruta de archivo de configuracion no valida.") # Invalid configuration file path.
            cfg = config.Config()
    else:
        cfg = config.Config()
    marker = Marker()
    board = Board(config=cfg)
        # display = Display(config=cfg, board=board, marker=marker)
    # terminal colors object
    c = config.Colors()

    print(c.YELLOW + "@Chan-Admin" + c.BLACK) # @Chan-admin
    while True:
        #cmdline(cfg, board, c)
        #signal.signal(signal.SIGINT, signal_handler)
        #try:
            cmdline(cfg, board, c)
        #except KeyboardInterrupt:
            #print (' Wut!? ')
            #sys.exit(0)
        #signal.pause()
