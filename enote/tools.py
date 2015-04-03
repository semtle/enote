#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Troels Kofoed Jacobsen

import sys, os, pickle, io
import html2text
import re
import string
from enmltohtml import enmltohtml

def htmltotxt(content):
    text = html2text.html2text(content)
    text = text.strip("\n")
    return re.sub(r"\n{2,}","\n", text)

def enmltotxt(content):
    return htmltotxt(enmltohtml(content))

def clean_filename(text):
    allowed = ' _-.()æøåÆØÅ%s%s'%(string.letters, string.digits)
    return ''.join([c for c in text if c in allowed])

class LogLevel:
    QUIET = 0
    DEFAULT = 1
    VERBOSE = 2

class Logger:
    def __init__(self, log_level=LogLevel.DEFAULT):
        self.log_level = log_level

    def log(self, text, log_level=LogLevel.DEFAULT):
        if log_level <= self.log_level:
            sys.stdout.write(text)
            sys.stdout.flush()

def mkdir(directory):
    # Not possible to mkdir to create all dirs in one go. Therefore need to
    # iterate through directory tree and create all non-existing dirs
    dirtree = directory.split("/")
    for i in range(2, len(dirtree) + 1):
        subpath = "/".join(dirtree[:i])
        if not os.path.isdir(subpath):
            os.mkdir(subpath)

def write_lastrun(basedir, curtime):
    f = io.open('%s/.enote.log'%(basedir,), 'wb')
    pickle.dump(curtime, f)
    f.close()

def read_lastrun(basedir):
    f = io.open('%s/.enote.log'%(basedir,), 'rb')
    lastrun = pickle.load(f)
    f.close()
    return lastrun
