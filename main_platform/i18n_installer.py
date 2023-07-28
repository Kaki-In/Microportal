#!/usr/bin/python3

import os, sys

class I18nInstaller():
    def __init__(self, langs, directory, i18n=True):
        self.langs = langs
        self.directory = directory
        self.i18n = i18n

    def loadDirectory(self, directory):
        path = os.path.abspath(directory)
        print(path)
        sep = os.path.sep
        s = path.split(sep)
        name = s[ -1 ] or s[ -2 ]

        for l in self.langs:
            if not l + ".i18n" in os.listdir(path):
                if "." + l + ".i18n" in os.listdir(path):
                    os.rename(path + sep + "." + l + ".i18n", path + sep + l + ".i18n")
                else:
                    a = open(path + sep + l + ".i18n", "w")
                    a.write("~LANGUAGE~ : " + l + "\n\n")
                    a.close()

        d = self.getDirectories(directory)

        ntit = name[ 0 ].upper() + name[ 1 : ]
        if self.i18n:
            i18n = open(path + sep + "i18n.py", "w")
            i18n.write("""
### FILE GENERATED BY A LOCAL_PROGRAM        ###
### PLEASE DON'T MODIFY THIS FILE, WHICH     ###
### WILL BE RE-GENERATED                     ###

import i18n_setup as _i18n\n""")

        subs = ""
        if d:
            if self.i18n:i18n.write("\n")
            for sd in d:
                sub = self.loadDirectory(path + sep + sd)
                if subs :
                   subs += ", "
                subs += "_get" + sub + "I18n()"
                if self.i18n:i18n.write("from .{name}.i18n import get{sub}I18n as _get{sub}I18n\n".format(name=sd, sub=sub))
        if self.i18n:
            i18n.write("\n")
            i18n.write("LANGUAGES = " + str(self.langs))
            i18n.write("""

def get{nameTitled}I18n():
    i18n = _i18n.I18NTranslator()

    for i in LANGUAGES:
        parser = _i18n.I18NFileParser(\"./{}.i18n\".format(i))
        i18n.addLanguage(parser.getLanguage())

    for subTranslator in [{i18nGet}]:
        i18n.loadFrom(subTranslator)

    return i18n

""".format("{}", nameTitled=ntit, i18nGet = subs))
            i18n.close()
        return ntit

    def getDirectories(self, directory):
        directories = []
        for i in os.listdir(directory):
            if os.path.isdir(directory + os.path.sep + i) and i != "__pycache__":
                directories.append(i)
        return directories

    def load(self):
        self.loadDirectory(self.directory)
        return 0

class I18nUninstaller():
    def __init__(self, directory, complete):
        self.directory = directory
        self.complete = complete

    def loadDirectory(self, directory):
        path = os.path.abspath(directory)
        print(path)
        sep = os.path.sep
        s = path.split(sep)
        name = s[ -1 ] or s[ -2 ]

        ldir = os.listdir(path)
        for i in ldir:
           fpath = path + sep + i
           print(fpath)
           if os.path.isdir(fpath) and i != "__pycache__":
               self.loadDirectory(fpath)
           elif i == "i18n.py":
               os.remove(fpath)
           elif i.endswith(".i18n"):
               if self.complete:
                   os.remove(fpath)
               else:
                   os.rename(fpath, path + sep + "." + i[ : -5 ].replace(".", '') + ".i18n")

    def load(self):
        self.loadDirectory(self.directory)
        return 0

def main(args):
    if len(args) > 1 and args[ 1 ] in ("-u", "--uninstall"):
        i = I18nUninstaller(os.path.curdir, "--complete" in args)
        return i.load()
    else:
        abis = args[ 1: ]
        while "--partial" in abis:
            abis.remove("--partial")
        i = I18nInstaller(abis, os.path.curdir, not "--partial" in args)
        return i.load()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
