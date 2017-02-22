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
# Assume the source folder containing generated code is:
# ~/acado/examples/code_generation/mpc_mhe/new_getting_started_export
#
# The target folder is current folder.
#
# ./acado_cgt_chip_rearrange.py /home/dang/acado/
# examples/code_generation/mpc_mhe/new_getting_started_export
#
# Author: Dang Doan
# Date: 2017.02.14

import sys
import os
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
os.system('cp '+source_dir+'/*.cpp .')
os.system('cp '+source_dir+'/*.h .')
os.system('cp '+source_dir+'/*.hpp .')
# qpoases source
os.system('cp '+source_dir+'/qpoases/INCLUDE/*.hpp .')
os.system('cp '+source_dir+'/qpoases/INCLUDE/EXTRAS/*.hpp .')
os.system('cp '+source_dir+'/qpoases/SRC/*.cpp .')
os.system('cp '+source_dir+'/qpoases/SRC/*.ipp .')
os.system('cp '+source_dir+'/qpoases/SRC/EXTRAS/*.cpp .')

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

txtMakefile = replace_in_list(txtMakefile, "./qpoases/SRC/EXTRAS", ".")
txtMakefile = replace_in_list(txtMakefile, "./qpoases/SRC", ".")
txtMakefile = replace_in_list(txtMakefile, "./qpoases/INCLUDE/EXTRAS", ".")
txtMakefile = replace_in_list(txtMakefile, "./qpoases/INCLUDE", ".")
txtMakefile = replace_in_list(txtMakefile, "./qpoases", ".")

objNewMakefile = open("newMakefile", "w")
objNewMakefile.writelines(txtMakefile)
objNewMakefile.close()

os.system('mv Makefile oldMakefile~')
os.system('mv newMakefile Makefile')

# 3. Modify the file SolutionAnalysis.cpp, change:
# #include <EXTRAS/SolutionAnalysis.hpp>
# to
# #include <SolutionAnalysis.hpp>

objFile = open("SolutionAnalysis.cpp", "r")
txtlines = objFile.readlines()
objFile.close()

txtlines = replace_in_list(txtlines, "EXTRAS/SolutionAnalysis.hpp", "SolutionAnalysis.hpp")

objFile = open("newSolutionAnalysis.cpp", "w")
objFile.writelines(txtlines)
objFile.close()

os.system('mv SolutionAnalysis.cpp oldSolutionAnalysis.cpp~')
os.system('mv newSolutionAnalysis.cpp SolutionAnalysis.cpp')

# 4.  Modify the file acado_qpoases_interface.cpp, change:
# #include "INCLUDE/QProblem.hpp"
# to
# #include "QProblem.hpp"
# and change:
# #include "INCLUDE/EXTRAS/SolutionAnalysis.hpp"
# to
# #include "SolutionAnalysis.hpp"

objFile = open("acado_qpoases_interface.cpp", "r")
txtlines = objFile.readlines()
objFile.close()

txtlines = replace_in_list(txtlines, "INCLUDE/QProblem.hpp", "QProblem.hpp")
txtlines = replace_in_list(txtlines, "INCLUDE/EXTRAS/SolutionAnalysis.hpp", "SolutionAnalysis.hpp")

objFile = open("newacado_qpoases_interface.cpp", "w")
objFile.writelines(txtlines)
objFile.close()

os.system('mv acado_qpoases_interface.cpp oldacado_qpoases_interface.cpp~')
os.system('mv newacado_qpoases_interface.cpp acado_qpoases_interface.cpp')
