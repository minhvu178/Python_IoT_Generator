#!/bin/bash

. ./.pws

export DEBUGLEVEL=0
# Debug Levels:
# 0 Debug       -> Allot of information will be printed, including printing site configuration to logfile.
# 1 Info        -> We just printing that processes is starting/ending
# 2 Warning     -> Will decide
# 3 Error       -> used in any try/except block
# 4 Critical    -> used when we going to kill the programm.

export ECHOCONFIG=1
export ECHORECORDS=0

export LOGGINGFILE=logger1.log

python3 app1/main.py
