#!/bin/bash

. ./.pws


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

export LOGGINGFILE=logger4c
export SEEDFILE=conf/Full4.json
export SITEIDS=101,105

# Data persistance will be controlled per site, using:
# sites["data_persistence"]
# 0 - no persist
# 1 - File based -> NOTE, if site is configured with file_debuglevel = 0, then it will be saved to logfile also.
# 2 - MongoDB Atlas

# If 1 => Specify Filename, we will add the date/time to filename to make it unique.
# If 2 -> Specify Mongo connection information in environment variables, or currently we do this via the .pwd file (listed in .gitignore)

export FILEROOT=sensor_metrics

python3 app4c/main.py
