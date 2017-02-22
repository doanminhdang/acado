#!/usr/bin/env python

# Tested with both Python 2.7.6 and Python 3.4.3
#
# This Python code rearrange the source code for testing ACADO
# code generation tool, so that all the source files are put
# under one directory at the same level.
#
# The idea is that when compiling code generated by ACADO for
# embedded platforms, when "make" does not fully function like
# on standard Linux platform, all the source code available in
# one directory would allow the compiler to process the code
# easier.
#
# Here are the steps, tested with this the example in
# acado/examples/code_generation/mpc_mhe/getting_started.cpp.
#
# Example usage:
# Assume the source folder containing generated code is: ~/acado/
# examples/code_generation/mpc_mhe/new_getting_started_qpoases3_export
#
# The target folder is current folder.
#
# ./acado_cgt_chip_qpoases3_rearrange.py /home/dang/acado/
# examples/code_generation/mpc_mhe/new_getting_started_qpoases3_export
#
# Author: Dang Doan
# Date: 2017.02.16

import sys
import os
import glob
from subprocess import call

# python2:
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

# python3:
# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
# Running "python commandfile.py arg1" yields 2 arguments.
# Running "commandfile.py arg1" also yields 2 arguments.

# call('ls')
# print(str(sys.argv[1]))
# call('ls '+str(sys.argv[1])) # using subprocess call does not work
# os.system('ls '+str(sys.argv[1])) # works ok

# 1. Bring all files inside folder getting_started_export to one folder.

source_dir = str(sys.argv[1])
os.system('cp '+source_dir+'/Makefile .')
os.system('cp '+source_dir+'/*.c .')  # including test.c
# os.system('cp '+source_dir+'/*.cpp .')
os.system('cp '+source_dir+'/*.h .')
# os.system('cp '+source_dir+'/*.hpp .')
# qpoases source
os.system('cp '+source_dir+'/qpoases3/include/qpOASES_e/extras/*.h .')
os.system('cp '+source_dir+'/qpoases3/include/qpOASES_e/*.h .')
os.system('cp '+source_dir+'/qpoases3/include/*.h .')
os.system('cp '+source_dir+'/qpoases3/src/*.c .')


# 2. Modify the Makefile: remove the folder structure.
objMakefile = open("Makefile", "r")
# txtMakefile = objMakefile.read()  # this command reads whole file as a string
txtMakefile = objMakefile.readlines()  # this command reads lines as a list
objMakefile.close()


def replace_in_list(text, oldwords, newwords):
    newlines = []
    # not necessary to split into words
    # for line in txtMakefile:
    #   words = line.split()
    #   newwords = ' '.join(words) + '\n'
    #   newlines = newlines + [newwords]
    for line in text:
        line = line.replace(oldwords, newwords)
        newlines = newlines + [line]
    return newlines

txtMakefile = replace_in_list(txtMakefile, "./qpoases3/src", ".")
txtMakefile = replace_in_list(txtMakefile, "./qpoases3/include", ".")
txtMakefile = replace_in_list(txtMakefile, "./qpoases3", ".")

objNewMakefile = open("newMakefile", "w")
objNewMakefile.writelines(txtMakefile)
objNewMakefile.close()

os.system('mv Makefile oldMakefile~')
os.system('mv newMakefile Makefile')

# 3. Modify .h and .c files of qpoases3:
# remove "qpOASES_e/extras/" in:
# #include <qpOASES_e/extras/...>
# and
# remove "qpOASES_e/" in:
# #include <qpOASES_e/...>

files = glob.glob("*.c")
for file in files:
    objFile = open(file, "r")
    txtlines = objFile.readlines()
    objFile.close()
    txtlines = replace_in_list(txtlines, "qpOASES_e/extras/", "")
    txtlines = replace_in_list(txtlines, "qpOASES_e/", "")
    objFile = open(file, "w")
    objFile.writelines(txtlines)
    objFile.close()

files = glob.glob("*.h")
for file in files:
    objFile = open(file, "r")
    txtlines = objFile.readlines()
    objFile.close()
    txtlines = replace_in_list(txtlines, "qpOASES_e/extras/", "")
    txtlines = replace_in_list(txtlines, "qpOASES_e/", "")
    objFile = open(file, "w")
    objFile.writelines(txtlines)
    objFile.close()
