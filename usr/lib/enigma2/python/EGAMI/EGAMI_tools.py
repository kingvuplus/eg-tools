# Patched by sodo
from boxbranding import getMachineBuild, getBoxType
from Components.config import config, configfile
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_SKIN, SCOPE_CURRENT_SKIN
from enigma import eConsoleAppContainer
import re, string
import os
from socket import *
import socket
from Components.About import about

def catalogXmlUrl():
    url = 'http://enigma-spark.com/egami/catalog_enigma2.xml'
    if getBoxType() in 'vusolo4k':
        url = 'http://enigma-spark.com/egami/catalog_enigma2_arm.xml'
    return url


def checkkernel():
    mycheck = 0
    if not fileExists('/media/usb'):
        os.system('mkdir /media/usb')
    if getMachineBuild() in ('7000s', '7100s', 'g300', 'hd2400', 'vusolo4k', 'vuduo2'):
        return 1
    if os.path.isfile('/proc/stb/info/vumodel') and os.path.isfile('/proc/stb/info/version'):
        if open('/proc/stb/info/vumodel').read().startswith('uno') or open('/proc/stb/info/vumodel').read().strip() == 'duo' or open('/proc/stb/info/vumodel').read().startswith('solo') or open('/proc/stb/info/vumodel').read().startswith('ultimo') or open('/proc/stb/info/vumodel').read().startswith('solo2') or open('/proc/stb/info/vumodel').read().startswith('duo2'):
            if about.getKernelVersionString() == '3.13.5' or about.getKernelVersionString() == '3.9.6':
                mycheck = 1
    else:
        mycheck = 0
    return mycheck


def preapreEmud():
    if not os.path.exists('/usr/tuxbox/config'):
        os.makedirs('/usr/tuxbox/config')
    if not fileExists('/etc/egami/emuname'):
        print '[EGAMI-EMUD] emuname file not exist! Creating it...'
        emuname_file = open('/etc/egami/emuname', 'w')
        emuname_file.write('Common Interface')
        emuname_file.close()
    else:
        print '[EGAMI-EMUD] emuname file exist'
    if not fileExists('/etc/egami/emunumber'):
        print '[EGAMI-EMUD] emunumber file not exist! Creating it...'
        emunumber_file = open('/etc/egami/emunumber', 'w')
        emunumber_file.write('1')
        emunumber_file.close()
    else:
        print '[EGAMI-EMUD] emunumber file exist'
    emulistxml = '<?xml version="1.0" encoding="iso-8859-1"?>\n<emulist>\n<emu emulator="Common Interface" osdname="DCCAMD" emuscript="/usr/emu_scripts/dccamd.xml" filecheck=""/>\n</emulist>'
    if not fileExists('/usr/tuxbox/config/emulist.xml'):
        print '[EGAMI-EMUD] emulist.xml file not exist! Creating it...'
        emunumber_file = open('/usr/tuxbox/config/emulist.xml', 'w')
        emunumber_file.write(emulistxml)
        emunumber_file.close()
    else:
        print '[EGAMI-EMUD] emulist.xml file exist'


def readEmuName():
    try:
        fp = open('/etc/egami/emuname', 'r')
        emuLine = fp.readline()
        fp.close()
        emuLine = emuLine.strip('\n')
        return emuLine
    except:
        return 'Common Interface'


def readEcmFile():
    try:
        ecmfile = file('/tmp/ecm.info', 'r')
        ecmfile_r = ecmfile.read()
        ecmfile.close()
        return ecmfile_r
    except:
        return 'ECM Info not aviable!'


def sendCmdtoEGEmuD(cmd):
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect('/tmp/egami.socket')
        print '[EG-EMU MANAGER] communicate with socket'
        s.send(cmd)
        s.close()
    except socket.error:
        print '[EG-EMU MANAGER] could not communicate with socket, lets try to start emud'
        cmd = '/bin/emud'
        runBackCmd(cmd)
        if s is not None:
            s.close()


def runBackCmd(cmd):
    eConsoleAppContainer().execute(cmd)


def getRealName(string):
    if string.startswith(' '):
        while string.startswith(' '):
            string = string[1:]

    return string


def hex_str2dec(str):
    ret = 0
    try:
        ret = int(re.sub('0x', '', str), 16)
    except:
        pass

    return ret


def norm_hex(str):
    return '%04x' % hex_str2dec(str)


def loadcfg(plik, fraza, dlugosc):
    wartosc = '0'
    if fileExists(plik):
        f = open(plik, 'r')
        for line in f.readlines():
            line = line.strip()
            if line.find(fraza) != -1:
                wartosc = line[dlugosc:]

        f.close()
    return wartosc


def loadbool(plik, fraza, dlugosc):
    wartosc = '0'
    if fileExists(plik):
        f = open(plik, 'r')
        for line in f.readlines():
            line = line.strip()
            if line.find(fraza) != -1:
                wartosc = line[dlugosc:]

        f.close()
    if wartosc == '1':
        return True
    else:
        return False


def unload_modules(name):
    try:
        from sys import modules
        del modules[name]
    except:
        pass


def wyszukaj_in(zrodlo, szukana_fraza):
    wyrazenie = string.strip(szukana_fraza)
    for linia in zrodlo.xreadlines():
        if wyrazenie in linia:
            return True

    return False


def wyszukaj_re(szukana_fraza):
    wyrazenie = re.compile(string.strip(szukana_fraza), re.IGNORECASE)
    zrodlo = open('/usr/share/enigma2/' + config.skin.primary_skin.value, 'r')
    for linia in zrodlo.xreadlines():
        if re.search(wyrazenie, linia) != None:
            return True

    zrodlo.close()
    return False
