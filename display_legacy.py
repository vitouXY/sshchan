#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Legacy (basic CLI) display module for sshchan.

Copyright (c) 2016
chibi <http://neetco.de/chibi>, makos <https://github.com/makos/>
under GNU GPL v2, see LICENSE for details
"""
# Edit port display_connected()
import math
import os
import re
import string
import subprocess
import time
from sys import exit

# Help texts and user guides
import helptexts

from pdata import getrandfile, getrandname, replacemotd, replacespa

THREADSPERPAGE = 10 # TODO - Move to the conf file

class DisplayLegacy:

    def __init__(self, config, board, c, marker):
        # Imports
        self.board = board
        self.config = config
        self.c = c
        self.marker = marker
        # The buffer of text used by laprint() and layout()
        self.buf = ''
        # HELPTEXTS
        self.helptext = helptexts.display_legacy_helptext
        self.userguide = helptexts.display_legacy_userguide

    def display_home(self):
        self.laprint(self.c.RED + 'Bienvenido a ' + self.c.YELLOW + '@Chan!\
            \n=============' + self.c.RED + '=========' + self.c.BLACK) # Welcome to 
        self.laprint(self.c.GREEN + 'SERVIDOR:\t' + self.c.BLACK + self.config.server_name)
        self.laprint(self.c.GREEN + 'MOTD:' + self.c.BLACK) # MOTD:
        self.print_motd()
        # Listing boards
        self.laprint(self.c.GREEN + "TABLEROS:" + self.c.BLACK) # BOARDS:
        self.laprint(self.board.list_boards())
        self.display_connected()
        self.layout()

    def laprint(self, *args, linestart='', end='\n', markup=False, line_limit=None):
        """Add the proper text to the buffer. Its companion function is layout()."""
        
        text = " ".join(args)
        if markup == True:
            text = self.marker.demarkify(text)

        text_newline_splits = text.splitlines(keepends=True)
        text = ''
        
        if type(line_limit) == int:
            for line in text_newline_splits[:line_limit]:
                text += linestart + line
            text.rstrip("\n")
        else:
            for line in text_newline_splits:
                text += linestart + line
            
        self.buf += text
        self.buf += end

    def layout(self):
        """Print out a page's worth of text in the buffer."""
        lines = 0
        chars = 0
 
        for c in self.buf:
            # Stops decoding errors
            c = c.encode("utf-8", "replace").decode("utf-8")
            if c in string.printable:
                chars += 1
            if c == '\n':
                chars = 0
                lines += 1
            if chars == self.config.tty_cols:
                chars = 0
                lines += 1
            print(c, end='')
            self.buf = self.buf[1:]
#            if lines == self.config.tty_lines - 2:
#                print(self.c.GREEN + "Page too long to display.", \
#                   "Type 'page' and hit Enter to see the rest." + self.c.BLUE)
#                lines += 1
#                break

        if lines <= self.config.tty_lines:
            lines_to_print = self.config.tty_lines - (lines + 1)
            print('\n' * lines_to_print, end='')

    def print_motd(self):
        """Prints the MOTD."""
        try:
            #m = open(self.config.motd)
            m = open(getrandfile(self.config.motd))
            motdbuf = m.read()
            motdbuf = replacemotd(motdbuf, self.config.port_ssh)
            m.close()
            self.laprint(motdbuf)     
        except FileNotFoundError:
            self.laprint("\'La publicacion de mierda nunca fue lo mismo\' --usuario de @Chan satisfecho") # 'Shitposting was never the same' --satisfied @Chan user

    def display_connected(self):
        """Prints out the number of people currently connected to the ssh port. edit_port sshd_config"""
        try:
            # self.config.port_ssh
            #connected = subprocess.check_output("netstat -atn | grep ':22' | grep 'ESTABLISHED' | wc -l", shell=True)
            #connected = subprocess.check_output("netstat -atn | grep ':" + self.config.port_ssh + "' | grep 'ESTABLISHED' | wc -l", shell=True)
            connected = subprocess.check_output("netstat -atn | grep 'ESTABLISHED' | awk '{print $4}' | grep ':" + self.config.port_ssh + "' | wc -l", shell=True)
            #connected = subprocess.check_output("w | awk '{print $1}' | grep 'anon' | wc -l", shell=True)
            connected = int(connected)
            self.laprint(self.c.YELLOW + "Conectado: " + self.c.BLACK + str(connected)) # Connected:
        except:
            self.laprint(self.c.YELLOW + "Conectado: " + self.c.BLACK + "Es un misterio") # Connected: ++ It is a mystery

    def display_help(self, cmd=None):
        """Display either the entire help message or just the help
        for a particular command (cmd)"""
        if cmd == None:
            # for : help
            for key in sorted(self.helptext.keys()):
                print(self.c.GREEN + self.helptext[key][0] + self.c.YELLOW, \
                    self.helptext[key][1] + "\n" + self.c.BLACK + self.helptext[key][2])
            print(helptexts.markup_helptext)
        else:
            # for : help <cmd>
            try:
                print(self.c.GREEN + self.helptext[cmd][0] + self.c.YELLOW, \
                    self.helptext[cmd][1] + "\n" + self.c.BLACK + self.helptext[cmd][2])
            except KeyError:
                print(self.c.RED + "No se pudo encontrar ayuda para ese comando." + self.c.BLACK) # Help for that command could not be found.

    def convert_time(self, stamp):
        """Convert UNIX timestamp to regular date format.

        @stamp - integer representing UNIX timestamp."""
        return str(time.strftime(
            '%H:%M:%S %d %b %Y',
            time.localtime(int(stamp))))

    def trip_convert(self, name):
        """Scans a name for a tripcode and converts it if so."""
        trip = re.split("##(?P<code>.*)", name)
        if (len(trip) > 1):
            #import zlib
            #name_proper = trip[0]
            #tripcode = zlib.crc32(trip[1])
            #digest = repr(tripcode) 
            #return name_proper + " !" + digest
            return name
        else:
            return name

    def display_board(self, page=1):
        """Displays the OPs of the threads on a board."""
        if self.board.name == '':
            print(self.c.RED + "No estas en un tablon." + self.c.BLACK) # You are not on a board.
            self.display_help(cmd="cd")
            return False

        # Checks if the path to the board's index file exists.
        # If it does not, the board most likely does not exist.
        if self.board.board_exists(self.board.name) == False:
            return False

        index = self.board.get_index()

        # Pagination
        hidden_pages = 0
        threads_number = len(index)
        last_page = 0
        if type(THREADSPERPAGE) == int and THREADSPERPAGE != 0:
            first_thread_to_display = (THREADSPERPAGE * page) - THREADSPERPAGE
            last_thread_to_display = (THREADSPERPAGE * page)
            if last_thread_to_display > threads_number: # Less than THREADPERPAGE threads on the board
                last_thread_to_display = threads_number
                first_thread_to_display = threads_number - THREADSPERPAGE
                if threads_number < THREADSPERPAGE:
                    first_thread_to_display = 0
            else:
                last_page = math.ceil(threads_number / THREADSPERPAGE)
                hidden_pages = last_page - page
        else:
            first_thread_to_display = 0
            last_thread_to_display = len(index)
        
        for x in reversed(range(first_thread_to_display, last_thread_to_display)): # reversed() makes newest threads appear at the bottom.
            thread = index[x]
            thread_id = thread[0]
            del thread
            self.display_thread(thread_id, index=index, op_only=True)
        self.layout()

        if hidden_pages >= last_page:
            print(self.c.RED + "No hay mas paginas para mostrar") # No more pages to display
        elif hidden_pages > 0:
            print(self.c.RED + str(hidden_pages) + " mas paginas, ingrese " + self.c.GREEN + "'p " + str((page + 1)) + "'" + self.c.RED + " para ver la siguiente pagina.") # ++ more pages, enter 'p ++'  to see the next page.


    def display_thread(self, thread_id, index=None, op_only=False, replies=1000):
        """Displays a thread.
        thread_id is self-explanatory.
        index: the thread index. It is an argument to cut down on reading
         the index file for every thread.
        op_only: if True, print only the OP post.
        replies is the number of replies to print."""
        if index == None:
            index = self.board.get_index()

        post_line_limit = None
        lst = "    "
        # The index of the thread in the index file
        thread_pos = self.board.thread_exists(int(thread_id))

        if thread_pos == -1: # -1 is the false return value for thread_exists()
            print(self.c.RED + 'Hilo no encontrado.' + self.c.BLACK) # Thread not found.
            return False
        
        else:
            thread = index[thread_pos]

        if op_only == True:
            replies = 1
            post_line_limit = 5
        
        posts = [thread[2]] + thread[3:][-replies:]
        
        op = True # Used to prepend lines with lst
        
        # print the subject
        self.laprint(self.c.RED + str(thread[1]) + self.c.BLACK)

        for reply in posts: # reversed() would the newest posts appear at the bottom
            if len(reply) == 3: # The old json format - just date, post_no and post_text
                name = getrandname() #"Anonymous"
                date = self.convert_time(int(reply[0]))
                post_no = str(reply[1])
                post_text = str(reply[2]).rstrip()
            else:
                name = reply[0] 
                date = self.convert_time(int(reply[1]))
                post_no = str(reply[2])
                post_text = str(reply[3]).rstrip()
            
            if not op:
                lst = ""
            
            self.laprint(self.c.YELLOW + name, end=' ', linestart=lst)
            self.laprint(self.c.GREEN + date + self.c.BLACK + ' No.' + post_no, end=' ')
            self.laprint()
            self.laprint(post_text, markup=True, line_limit=post_line_limit, linestart=lst)
            
            op = False

        if op_only == True:
            self.laprint(self.c.GREEN + str(len(thread) - 3), "respuestas \
ocultas. Escribe \'v " + str(thread_id) + "\' para verlos.\n") # ++ replies hidden. Type 'v ++' to view them.

        return True

    def post_menu(self, thread_id=-1):
        """Get post from the user and send it to addPost()."""
        # Get name. Default is the username of the controlling user of
        # the sshchan process.
        name = str(input("Nombre: [por defecto: " + self.c.YELLOW + \
self.config.username + self.c.BLACK + "] ")) # Name: [default:
        if name == '':
            name = self.config.username
        else:
            name = replacespa(name)
            name = self.trip_convert(name)

        # Get the post text.
        print("Publicar texto:\n" + self.c.GREEN + \
"[Sugerencia: deja una linea en blanco para completar la publicacion.]" + self.c.BLACK) # Post text: ++ [Hint: leave a blank line to complete the post.]
        post_text = ''
        blanks = 0 # How many blank lines have been entered

        while True:
            line = input()
            if line == '':
                blanks += 1
            else:
                blanks = 0
            if blanks == 2:
                break 
            post_text += line + "\n"

        # If the user did not post anything, show an error.
        if post_text == '\n':
            print(self.c.RED + "Has hecho un mensaje vacio. Scrapping..." \
+ self.c.BLACK) # You have made an empty post. Scrapping...
            return False

        post_text = replacespa(post_text)
        post_text = post_text.rstrip()

        if thread_id == -1: # If a new thread is to be posted
            subject = str(input("Titulo: ")) # Subject:
        else:
            subject = ""

        subject = replacespa(subject)

        name = self.marker.esc(name)
        subject = self.marker.esc(subject)
        post_text = self.marker.esc(post_text)

        success = self.board.add_post(post_text, name=name, \
                  subject=subject, thread_id=thread_id)
        if success == True:
            print(self.c.GREEN + "Publicacion exitosa!" + self.c.BLACK) # Post successful!
        else:
            print(self.c.RED + "Publicacion fallida." + self.c.BLACK) # Post failed.
