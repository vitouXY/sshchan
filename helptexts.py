#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""All the long and ugly-looking helptexts go here."""
from config import Colors as c
from chan_mark import Marker as marker

admin_helptext = \
c.RED + "Ayuda de @Chan-Admin\n" \
+ c.GREEN + "add" + c.YELLOW + " [nombre] [descripcion]\n" \
+ c.BLACK + "Agrega un tablero con [nobre] y [descripcion]\n\
No uses barras, se agregan automaticamente.\n" \
+ c.GREEN + "config" + c.YELLOW + " [opcion] [nuevo valor]\n" \
+ c.BLACK + "Cambia el valor de la [opcion] a un [nuevo valor] en el archivo de configuracion atchan.conf.\n" \
+ c.GREEN + "list|ls\n" \
+ c.BLACK + "Lista de tableros\n" \
+ c.GREEN + "lsconfig\n" \
+ c.BLACK + "Lista las opciones de configuracion actuales\n" \
+ c.GREEN + "rename" + c.YELLOW + " [nombre] [nueva descripcion]\n" \
+ c.BLACK + "Cambia la descripcion del tablero [nombre] a una [nueva descripcion]\n" \
+ c.GREEN + "rm" + c.YELLOW + " [tablero] [no. de publicacion]\n" \
+ c.BLACK + "Elimina la publicacion con el no. en el tablero\n" \
+ c.GREEN + "rmboard" + c.YELLOW + " [nombre]\n" \
+ c.BLACK + "Elimina el tablero [nombre]\n" \
+ c.GREEN + "exit\n" \
+ c.BLACK + "Sale de @Chan-Admin"
#@Chan-admin help
#[name] [description]
#adds a board with [name] and [description]
#don't use slashes, they're added automatically.
#[option] [new value]
#changes [option]'s value to [new value] in the atchan.conf config file.
#lists boards
#lists current configuration options
#[name] [new description]
#changes the description of board [name] to [new description]
#[board] [post no.]
#removes the post with post no. on board
#[name]
#deletes board [name]
#exits @Chan-admin


display_legacy_helptext = \
{"exit": ["exit | q | quit", "",  "Sale de @Chan. No toma argumentos."],\
 "help": ["h | help", "[] | [comando]", "Muestra un mensaje de ayuda."],\
 "cd": ["b | board | cd", "[nombre de tablero]", "Muestra el tablero dado."],\
 "ls":["ls | list", "", "Lista de tableros."],\
 "page": ["p | page", "[no. de pagina]", "Elija la pagina de un tablero para mostrar."],\
 "view": ["v | view", "[no. de hilo/publicacion]", "Muestra un hilo."],\
\
 "re": ["re | reply", "[] | [nombre de tablero] | [no. de hilo]",\
 "Responde a un hilo o crea uno nuevo.\n\
@Chan/tablero/> re " + c.GREEN + "# Publica un nuevo hilo en /tablero/\n" \
+ c.BLACK + "@Chan/tablero/> re 1 " + c.GREEN + "# Responde al hilo no.1\n" \
+ c.BLACK + "@Chan/tablero/1> re " + c.GREEN + \
"# Responde al hilo no.1 con el texto dado." + c.BLACK \
],\
 "refresh": ["refresh | rb", "", "Actualiza el tablero actual."],\
 "rt": ["rt", "", "Actualiza el hilo actual."],\
 "V": ["V | version", "", "Muestra el numero de version."],\
}
#"re": ["re | reply", "[nombre de tablero] | [[no. de hilo] [[texto]]]",\
#Quits @Chan. Takes no arguments.
#[command] ++ Prints a help message.
#[board name] ++ Displays the given board.
#List boards
#[page no.] ++ Choose which page of a board to display.
#[thread/post no.] ++ Displays a thread.
#[board name] | [[thread no.] [[text]]]
#Replies to a thread or creates a new one.
#Posts a new thread to /board/
#Replies to thread no.1
#Replies to thread no.1 with the given text.
#Refreshes the current board.
#Refreshes the current thread.
#Print version number

markup_helptext = \
c.PURPLE + "\nAyuda de marcado:\n" + c.BLACK + \
"\'\'\'text\'\'\' ---> " + "\033[4mtext\033[0m [subrayado]\n" + \
"**text** -----> " + "\033[1mtext\033[0m [negrita]\n" + \
"__text__ -----> " + "\033[3mtext\033[0m [italica]\n" + \
"~~text~~ -----> " + "\033[9mtext\033[0m [tachado]\n" + \
"==text== -----> " + "\033[7mtext\033[0m [video inverso]\n" + \
"--text-- -----> " + "\033[2mtext\033[0m [negativo oscuro]\n" + \
">>text<< -----> " + "\033[0;30;40mtext\033[0m [spoiler]"
#Markup help:
#[bold] negrita
#[strikethrough] tachado
#[reverse video] inverso

display_legacy_userguide = \
c.YELLOW + "@Chan: " + c.BLACK + "una guia del usuario\n" + \
"Cuando entras por primera vez en @Chan, veras un simbolo del sistema como este:\n" + \
c.BLUE + "\t@Chan///>\n\n" + c.BLACK + \
"Esas barras son significativas. Te muestran donde estas en el chan segun \
este esquema:\n" + \
c.BLUE + "\t@Chan/" + c.YELLOW + "[TABLERO]" + c.BLUE + "/" + \
c.YELLOW + "[NO. de HILO]" + c.BLUE + "/>\n\n" + \
c.BLACK + "Use el comando \'cd\' para ir a diferentes tableros:\n" + \
c.BLUE + "\t@Chan///>" + c.BLACK + " cd /meta/\n" + \
c.YELLOW + "\t***muestra hilos en el tablero***\n" + \
c.BLUE + "\t@Chan/meta//>\n\n" + \
c.BLACK + "Puedes actualizar el tablero actual con el comando \'refresh\':\n" + \
c.BLUE + "\t@Chan/meta//> " + c.BLACK + "refresh\n\n" + \
"Puedes ir a un hilo con el comando \'v\':\n" + \
c.BLUE + "\t@Chan/meta//>" + c.BLACK + " v 1\n" + \
c.YELLOW + "\t***muestra el hilo no.1***\n" + \
c.BLUE + "\t@Chan/meta/" + c.PURPLE + "1" + c.BLUE + "/>\n\n" + \
c.BLACK + "Esto te muestra el hilo. O, si ingresas el numero de publicacion de una respuesta, se mostrara \
el hilo del que provino esa respuesta.\n"
# a user's guide
# When you first enter @Chan, you'll see a command prompt like this:
# Those slashes are significant. They show you where you are on the chan according to this scheme:
# [BOARD]
# [THREAD NO.]
# Use the 'cd' command to go to different boards:
# displays threads on the board
# One can refresh the current board with the 'refresh' command
# You can go to a thread with the 'v' command:
# displays thread no.1
# This shows you the thread. Or, if you put in a reply's post number, it will show the thread from which that reply came.
