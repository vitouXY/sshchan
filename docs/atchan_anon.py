#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/python3
#qpy:console
import os,sys
import time
import signal
def keyboardInterruptHandler(signal, frame ):
    print( "KeyboardInterrupt (ID: {}) has been caught. Cleaning up..." . format(signal ))
    exit(0)
signal.signal(signal.SIGINT, keyboardInterruptHandler)

def main(var_path, var_py, var_cfg):
    if(os.path.exists(var_path)):
        #os.chdir(var_path)
        #os.system('pwd')
        os.system('cd ' + var_path + ' && /usr/bin/python3 ' + var_py + ' ' + var_cfg)
        #time.sleep(1)
    #return main(var_path, var_py, var_cfg)

if __name__ == '__main__':
    #   (  Edit this path , ... , ... )
    main('/srv/chan/', "sshchan.py", "atchan.conf")
    sys.exit(0)
