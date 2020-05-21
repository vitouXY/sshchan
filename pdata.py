#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Edit replacemotd() and/or names[] ...
"""
import os
from random import choice
#from pdata import getrandname
#from pdata import getrandfile
#from pdata import replacemotd
#from pdata import replacespa

def replacespa(text):
    """
    display_legacy.py :
      #post_text = replacespa(post_text)
      post_text = self.marker.esc(post_text)
    """
    esp = dict()
    esp = {
 'ñ':'n', 'Ñ':'N', 
 'á':'a', 'Á':'A', 'ā':'a', 'A':'A', 'ä':'a', 'Ä':'A', 'à':'a', 'À':'A', 'Â':'A', 'â':'a',
 'é':'e', 'É':'E', 'e':'e', 'E':'E', 'ë':'e', 'Ë':'E', 'è':'e', 'È':'E', 'Ê':'E', 'ê':'e',
 'í':'i', 'Í':'I', 'i':'i', 'I':'I', 'ï':'i', 'Ï':'I', 'ì':'i', 'Ì':'I', 'Î':'I', 'î':'i',
 'ó':'o', 'Ó':'O', 'ō':'o', 'Ō':'O', 'ö':'o', 'Ö':'O', 'ò':'o', 'Ò':'O', 'Ô':'O', 'ô':'o',
 'ú':'u', 'Ú':'U', 'ū':'u', 'Ū':'U', 'ü':'u', 'Ü':'U', 'ù':'u', 'Ù':'U', 'Û':'U', 'û':'u'
    }
    for i,ii in esp.items():
        text=text.replace( str(i), str(ii) )
    text = text.encode( "ascii", "replace" ).decode() # 'replace' for '?' | 'ignore' for ''
    return text


def getrandfile(filename):
    if (os.path.isfile(filename)):
        # return motd file
        return filename
    else:
        # return x motd file from motd directory
        #if (os.path.exists(filename + '/')):
        var_path = filename + '/'
        var_file = choice([xi for xi in os.listdir(var_path) if os.path.isfile(os.path.join(var_path, xi))])
        #print("File {}...".format(file))
        return os.path.join(var_path, var_file)


def _readtorhostname(tordir='/var/lib/tor/'):  # not Tested
    mdata = None
    if (os.path.exists(tordir) and os.path.isfile(tordir+'hostname')):
        m = open(tordir+'hostname')
        mdata = m.readline().replace( "\n" , '' )
        m.close()
    if (mdata == '' or mdata == None): #if (mdata is '' or mdata is None):
        return '<onion>'
    else:
        return mdata #+'.onion'


def replacemotd(motdbuf, port_ssh):
   """ Replace '{host}' string in motd file for value... """
   """                      ( ... ,      Edit this values ! ) """
   motdbuf = motdbuf.replace( '{host}' , 'localhost' )
   #motdbuf = motdbuf.replace( '{port}' , '22' )
   motdbuf = motdbuf.replace( '{port}' , port_ssh )
   motdbuf = motdbuf.replace( '{ohost}' , _readtorhostname('/var/lib/tor/hidden_service/') )
   motdbuf = motdbuf.replace( '{oport}' , '<onion>' )
   motdbuf = motdbuf.replace( '{user}' , 'anon' )
   motdbuf = motdbuf.replace( '{pass}' , 'anon' )
   return motdbuf


def getrandname():
    #str(choice(range(0,9999)))
    return choice(names)

names = [
    'Anonymous',
    'Anonim'+choice(['a','o']),
    'Usuari'+choice(['a','o']),
    'Elf'+choice(['a','o']),
    'Aldean'+choice(['a','o']),
    'Bolivian'+choice(['a','o']),
    'Peruan'+choice(['a','o']),
    'Chilen'+choice(['a','o']),
    'Argentin'+choice(['a','o']),
    'Venezolan'+choice(['a','o']),
    'Colombian'+choice(['a','o']),
    'Mexican'+choice(['a','o']),
    'Goblin',
    'Wizard',
    'Choroy',
    'Chimuelo',
    'Aldo',
    'Adolfo',
    'Alpha',
    'Beta',
    'Epsilon',
    'Omega',
    'Zeta',
    'Pikachu',
    'Onii-Chan',
    'Imouto',
    'Aniki',
    'Pedo',
    'Ochinchin',
    'Oppai',
    'Omanko',
    'Otaku',
    'Unknown',
    'Shiro',
    'Shonen',
    'Lain',
    'Neko',
    'Shinigami',
    str(choice(range(1,99)))+choice(['-','+'])+str(choice(range(1,99)))+'='+str(choice(range(1,99))),
    str(choice(range(1000,9999))),
    'Anon'+choice(['','_'+str(choice(range(100,999)))]),
    'User'+choice(['','_'+str(choice(range(100,999)))]),
    'Vegeta'+choice(['',str(choice(range(1,9)))+'7']),
    'MP '+choice(['-','+'])+str(choice(range(0,9999))),
    'HP '+choice(['-','+'])+str(choice(range(0,9999))),
    'EXP '+choice(['-','+'])+str(choice(range(0,9999))),
    'Lv. '+str(choice(range(1,100))),
    'Mob '+str(choice(range(0,100)))+'.'+str(choice(range(0,9)))+'%',
    'Dado['+str(choice(range(1,6)))+']',
    'Dado['+str(choice(range(1,6)))+']['+str(choice(range(1,6)))+']',
    'Barto',
    'John Doe',
    'Jane Doe',
    'Supa Hacka',
    'Padawan',
    'Muggles',
    'Kid',
    'Boy',
    'Old',
    'Man',
    'Woman',
    'TuTuRu~',
]

#print(getrandname())

