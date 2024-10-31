#!/bin/bash

. ./.pws

# General Level
# Debug Levels:
# 0 Debug       -> Allot of information will be printed, including printing site configuration to logfile.
# 1 Info        -> We just printing that processes is starting/ending
# 2 Warning     -> Will decide
# 3 Error       -> used in any try/except block
# 4 Critical    -> used when we going to kill the programm.

# Console Handler
export CONSOLE_DEBUGLEVEL=0
# File Handler
export FILE_DEBUGLEVEL=0

export LOGGINGFILE=logger3a
export SEEDFILE=conf/Full3a.json
export SITEIDS=101,102,103,105

python3 app3a/main.py
