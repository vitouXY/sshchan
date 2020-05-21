#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Markup class allows the use of easy-to-write characters to style the text
instead of using escape codes.

==text== --> reverse video
'''text''' --> underline
~~text~~ --> strikethrough
**text** --> bold
__text__ --> italic
--text-- --> negative dark
>>text<< --> spoiler

Copyright (c) 2015
makos <https://github.com/makos>, chibi <http://neetco.de/chibi>
under GNU GPL v2, see LICENSE for details
"""

import re
import string

class Marker():

    def esc(self, input_text):
        output_text = ''
        for c in input_text:
            if c not in string.printable + string.whitespace:
                output_text += '\\' + str(ord(c))
            else:
                output_text += c
        return output_text

    def demarkify(self, input_text):
        """Prints out a marked-up piece of text."""
        output_text = self.esc(input_text)
        # ~~XY~~ strikethrough
        output_text = re.sub(
            '~~(?P<substring>.*?)~~', '\033[0;9m\g<substring>\033[0m',
            output_text)
        # '''XY''' underline
        output_text = re.sub(
            '\'\'\'(?P<substring>.*?)\'\'\'', '\033[0;4m\g<substring>\033[0m',
            output_text)
        # ==XY== rv
        output_text = re.sub(
            '==(?P<substring>.*?)==', '\033[0;7m\g<substring>\033[0m',
            output_text)

        # __XY__ italic
        output_text = re.sub(
            '__(?P<substring>.*?)__', '\033[0;3m\g<substring>\033[0m',
            output_text)
        # --XY-- negative
        output_text = re.sub(
            '--(?P<substring>.*?)--', '\033[0;2m\g<substring>\033[0m',
            output_text)
        # **XY** bold
        output_text = re.sub(
            '\*\*(?P<substring>.*?)\*\*', '\033[0;1m\g<substring>\033[0m',
            output_text)
        # >>XY<< spoiler
        output_text = re.sub(
            '\>\>(?P<substring>.*?)\<\<', '\033[0;30;40m\g<substring>\033[0m',
            output_text)

        return output_text

# '\x1b[9;32m \x1b[0m \033[9;31;42m \033[0m'
## 0 ... 9 Style
# 0 Normal
# 1 Negrita brillante
# 2 negativo1 oscuro
# 3 Italica
# 4 Subrayado
# 5 negativo2 claro
# 6
# 7 Inverso
# 8 Invisible
# 9 Tachado
## 30 ... 37 FG Color
## 40 ... 47 BG Color
# 0 Negro
# 1 Verde
# 2 Rojo
# 3 Amarillo
# 4 Azul
# 5 Purpura
# 6 Blanco
