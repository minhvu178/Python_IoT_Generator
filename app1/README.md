# Python based IoT SimeSeries data generator

## Overview

In this first app we will simply show how we will set environment varables and read them in.

Secondly we will introduce our Logging framework.


### Environment Variables

Re environment variables, this is my way of defining and using them, I like to use this, as for simple local running I can set the variables in the run.sh file. If I was to containerize/dockerize the app then I can pass the variable in at the command line using the -e instruction or set them in the docker-compose.yaml file in the environment section or specify them in the .env file and then use the environment variable. 

If we're deploying on Kubernetes then it becomes part of the service/pod deployment. the big thing, but for me, all of these methods of passing variables in, does not require any code change.

I know there are options like load_env and others, this is simply the way I've standardized things on for myself as it works for me.

### Logging

This is my implimentation/wrapping of the logging framework that we will use throughout the project, just to make the logs pretty... more productionable looking. It's nothing special here. Simply a implimentation of logging package, configured with 2 handlers, a console handler and a file handler.

Re the logging levels... It's a bit counter intuitive, but the higher the number the more less the logging level.

I specify the level as a debug level number, which is then translated into a logging level.

DebugLevels           logging.setlevel 
    - 0                 Debug           -> Allot of information will be printed, including printing site configuration to logfile.
    - 1                 Info            -> We just printing that processes is starting/ending
    - 2                 Warning         -> Will decide
    - 3                 Error           -> used in any try/except block
    - 4                 Critical        -> used when we going to kill the program.

    Now something to be aware of, level 4 means only messages at critical level will be printed, level 3 means all error and critical, and so on until we get to level 0 / debug which means you better be a fast reader... ;)