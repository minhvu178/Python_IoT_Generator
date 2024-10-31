#######################################################################################################################
#
#
#  	Project     	    : 	IoT based TimeSeries Data via Python Application 
#
#   File                :   main.py
#
#   Description         :   Basic scafolding showing how we provide configuration variables and how our 
#                       :   console and file logger works.
#
#   Created     	    :   18 October 2024
#
#   Changelog           :   See bottom
#
#   JSON Viewer         :   https://jsonviewer.stack.hu
#
#   Mongodb             :   https://www.mongodb.com/cloud/atlas      
#                       :   https://hub.docker.com/r/mongodb/mongodb-atlas-local
#
#   Create Virtualenv   :   /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m venv ./venv
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "2.0.6.1"
__copyright__   = "Copyright 2024, - G Leonard"


import utils


config_params   = utils.configparams()
logger          = utils.logger(config_params)

def main():
    
    if config_params["ECHOCONFIG"] == 1: 
        
        utils.echo_config(config_params, logger)
    
    #end if
    
    logger.debug('Hello, This is a Debug (level=0) Message with no variables added.')


    # Quick Example of how we can print a info message to the console, no added variables
    logger.info('Hello, This is a Info (level=1) Message with no variables added.')

    # same as above but we now add a variable to include/append to our text, the {logfile} variable does not need to be at the end of the line either.
    logger.info('Hello, this is a Info (level=1) message with a single variable : {logfile}'.format(
        logfile=config_params["LOGGINGFILE"]
    ))
    
    # Here we show as per above, but 2 variables and we show how a variable can be mid sentence.
    logger.info('Hello, this is a {message} (level=1) message with a two variables : {logfile}'.format(
        message="Info",
        logfile=config_params["LOGGINGFILE"]
    ))
        
    # Quick Example of how we can print a warning message to the console
    logger.warning('Hello, this is a Warning (level=2) message with a single variable : {logfile}'.format(
        logfile=config_params["LOGGINGFILE"]
    ))

    # Quick Example of how we can print a error message to the console
    logger.error('Hello, this is a Error message (level=3) with a single variable : {logfile}'.format(
        logfile=config_params["LOGGINGFILE"]
    ))

    # Quick Example of how we can print a critial message to the console
    logger.critical('Hello, this is a Critical (level=4) message with a single variable : {logfile}'.format(
        logfile=config_params["LOGGINGFILE"]
    ))
        
# end main

if __name__ == "__main__":

    main()