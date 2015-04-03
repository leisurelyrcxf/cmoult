#    fiderouter.py This file is part of Pymoult
#    Copyright (C) 2013 Sébastien Martinez, Fabien Dagnat, Jérémy Buisson
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
"""pymoult.highlevel.finderouter.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides tools for quiering and intropecting a running
   application.

"""

import inspect
import sys
import types
import __builtin__

header = "query"

#List of all modules provided by Python (as listed here : https://docs.python.org/2.7/py-modindex.html)

pymodules = ["__builtin__","__future__","__main__ ","_winreg","abc","aepack","aetools","aetypes","aifc","al","AL","anydbm","applesingle","argparse","array","ast","asynchat","asyncore","atexit","audioop","autoGIL","base64","BaseHTTPServer","Bastion","bdb","binascii","binhex","bisect","bsddb","buildtools","bz","calendar","Carbon","cd","cfmfile","cgi","CGIHTTPServer","cgitb","chunk","cmath","cmd","code","codecs","codeop","collections","ColorPicker","colorsys","commands","compileall","compiler","ConfigParser","contextlib","Cookie","cookielib","copy","copy_reg","cPickle","cProfile","crypt","cStringIO","csv","ctypes","curses","datetime","dbhash","dbm","decimal","DEVICE","difflib","dircache","dis","distutils","dl","doctest","DocXMLRPCServer","dumbdbm","dummy_thread","dummy_threading","EasyDialogs","email","encodings","ensurepip","errno","exceptions	","fcntl","filecmp","fileinput","findertools","FL","fl","flp","fm","fnmatch","formatter","fpectl","fpformat","fractions","FrameWork","ftplib","functools","future_builtins","gc","gdbm","gensuitemodule","getopt","getpass","gettext","gl","GL","glob","grp","gzip","hashlib","heapq","hmac","hotshot","htmlentitydefs","htmllib","HTMLParser","httplib","ic","icopen","imageop","imaplib","imgfile","imghdr","imp","importlib","imputil","inspect","io","itertools","jpeg","json","keyword","lib2to3","linecache","locale","logging","macerrors","MacOS","macostools","macpath","macresource","mailbox","mailcap","marshal","math","md5","mhlib","mimetools","mimetypes","MimeWriter","mimify","MiniAEFrame","mmap","modulefinder","msilib","msvcrt","multifile","multiprocessing","mutex","Nav","netrc","new","nis","nntplib","numbers","operator","optparse","os","ossaudiodev","parser","pdb","pickle","pickletools","pipes","PixMapWrapper","pkgutil","platform","plistlib","popen2","poplib","posix","posixfile","pprint","profile","pstats","pty","pwd","py_compile","pyclbr","pydoc","Queue","quopri","random","re","readline","resource","rexec","rfc822","rlcompleter","robotparser","runpy","sched","ScrolledText","select","sets","sgmllib","sha","shelve","shlex","shutil","signal","SimpleHTTPServer","SimpleXMLRPCServer","site","smtpd","smtplib","sndhdr","socket","SocketServer","spwd","sqlite3","ssl","stat","statvfs","string","StringIO","stringprep","struct","subprocess","sunau","sunaudiodev","SUNAUDIODEV","symbol","symtable","sys","sysconfig","syslog","tabnanny","tarfile","telnetlib","tempfile","termios","test","textwrap","thread","threading","time","timeit","Tix","Tkinter","token","tokenize","trace","traceback","ttk","tty","turtle","types","unicodedata","unittest","urllib","urllib2","urlparse","user","UserDict","UserList","UserString","uu","uuid","videoreader","W","warnings","wave","weakref","webbrowser","whichdb","winsound","wsgiref","xdrlib","xml","xmlrpclib","zipfile","zipimport","zlib","opcode","tputil","sre_constants","sre_parse","sre_compile","genericpath","posixpath","_weakrefset","alt","_abcoll","_structseq"]

class AppModel(object):
    def __init__(self,filter):
        self.modules = {}
        self.filter = filter
        self.generate()
        
    def generate(self):
        all_modules = getModules(filter = self.filter)
        for modname in all_modules:
            mod = sys.modules[modname]
            self.modules[modname] = {'functions':[],'globals':[],'classes':{},'modules':[]}
            content = getModuleContent(mod)
            for itemname in content:
                item = mod.__dict__[itemname]
                if type(item) == types.ClassType:
                    #The item is a class (not a type)
                    self.modules[modname]['classes'][itemname] = self.parse_class(item)
                elif type(item) == __builtin__.type:
                    #The item is a Type (not a classType)
                    self.modules[modname]['classes'][itemname] = self.parse_class(item)
                elif type(item) == types.FunctionType:
                    #The item is a function
                    self.modules[modname]['functions'].append(itemname)
                elif type(item) == types.ModuleType:
                    #The item is a module
                    self.modules[modname]['modules'].append(itemname)
                else:
                    #The item is a global variable
                    self.modules[modname]['globals'].append(itemname)

    def parse_class(self,cls):
        cls_model = {'methods':[],'attributes':[]}
        for item in cls.__dict__:
            if not (item.startswith('__') and item.endswith('__')):
                if type(cls.__dict__[item]) == types.FunctionType:
                    #The item is a method
                    cls_model['methods'].append(item)
                else:
                    #The item is an attribute
                    cls_model['attributes'].append(item)
        return cls_model

                
    def __str__(self):
        string = ""
        for module in self.modules:
            string+=module+"\n"+"="*len(module)+"\n"
            #Add the modules
            string+="\n\tLoaded Modules\n\t--------------\n"
            for mod in self.modules[module]['modules']:
                string+="\t"+mod+"\n"
            #Add the globals
            string+="\n\tGloabal Variables\n\t-----------------\n"
            for var in self.modules[module]['globals']:
                string+="\t"+var+"\n"
            #Add the functions
            string+="\n\tFunctions\n\t----------\n"
            for fun in self.modules[module]['functions']:
                string+="\t"+fun+"\n"
            #Add the classes
            string+="\n\tClasses\n\t-------\n"
            for cls in self.modules[module]['classes']:
                string+="\t"+cls+"\n\t"+"+"*len(cls)+"\n"
                string+="\t\tAttributes\n\t\t----------\n"
                for attr in self.modules[module]['classes'][cls]['attributes']:
                    string+="\t\t"+attr+"\n"
                string+="\n\t\tMethods\n\t\t-------\n"
                for method in self.modules[module]['classes'][cls]['methods']:
                    string+="\t\t"+method+"\n"
            string+="\n"
        return string

#Visiteur pour analyser l'app selon la vue "métier"
                

def getModules(filter="a"):
    """gets the names of all loaded modules according to the given filter.
    The filter can be any combination of the given letters:
    a : the application modules
    b : the builtin modules
    l : the Python libraries modules
    m : the pymoult libraries 
    python : gets the application modules plus the loaded Python library modules
    all : gets everything
    """                                                 
    modules = []
    for modname in sys.modules:
        if sys.modules[modname] is not None: 
            firstname = modname.split('.')[0]
            if firstname in sys.builtin_module_names:
                if "b" in filter:
                    modules.append(modname)
            elif firstname in pymodules:
                if "l" in filter:
                    modules.append(modname)
            elif firstname == "pymoult":
                if "m" in filter:
                    modules.append(modname)
            elif "a" in filter:
                modules.append(modname)
    return modules

def lookupModule(name):
    """Looks up a module in loaded modules"""
    if name in sys.modules.keys():
        return sys.modules[name]
    else:
        return None

def getModuleContent(module):
    """Return the names of every top-level content of the given module"""
    content = []
    for attr in module.__dict__:
        if not (attr.startswith("__") and attr.endswith("__")):
            content.append(attr)
    return content


def parseCommand(command):
    if command.startswith(header):
        query = command[len(header)+1:].strip()
        if query.startswith("model"):
            model_filter = query[5:].strip()
            print(AppModel(model_filter))
            
        
