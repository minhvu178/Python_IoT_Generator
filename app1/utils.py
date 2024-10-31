
#######################################################################################################################
#
#
#  	Project     	: 	TimeSeries Data via Python Application stored in MongoDB Timeseries Collection
#
#   File            :   utils.py
#
#   Description     :   Some common utility functions
#
#
#   Created     	:   18 October 2024
#
#   Changelog       :   See bottom
#
#   JSON Viewer     :   https://jsonviewer.stack.hu
#
#   Mongodb         :   https://www.mongodb.com/cloud/atlas      
#                   :   https://hub.docker.com/r/mongodb/mongodb-atlas-local
#
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "2.0.6.1"
__copyright__   = "Copyright 2024, - G Leonard"


import logging, os


def logger(config_params):
    
    # Logging Handler
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    fh = logging.FileHandler(config_params["LOGGINGFILE"])

    if config_params["DEBUGLEVEL"] == 0:
        ch.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
        
    elif config_params["DEBUGLEVEL"] == 1:
        ch.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)
        
    elif config_params["DEBUGLEVEL"] == 2:
        ch.setLevel(logging.WARNING)
        fh.setLevel(logging.WARNING)
        
    elif config_params["DEBUGLEVEL"] == 3:
        ch.setLevel(logging.ERROR)
        fh.setLevel(logging.ERROR)
        
    elif config_params["DEBUGLEVEL"] == 4:
        ch.setLevel(logging.CRITICAL)
        fh.setLevel(logging.CRITICAL)
        
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# end logger

def configparams():
    
    config_params = {}
    
    # General
    config_params["DEBUGLEVEL"]     = int(os.environ["DEBUGLEVEL"])
    config_params["ECHOCONFIG"]     = int(os.environ["ECHOCONFIG"])
    config_params["ECHORECORDS"]    = int(os.environ["ECHORECORDS"])
    config_params["LOGGINGFILE"]    = os.environ["LOGGINGFILE"]
    
    return config_params

# end configparams

def echo_config(config_params, logger):
    
    
    logger.info("***********************************************************")
    logger.info("* ")
    logger.info("*          Python IoT Sensor data generator")
    logger.info("* ")
    logger.info("***********************************************************")
    logger.info("* General")
    logger.info("* DebugLevel                : "+ str(config_params["DEBUGLEVEL"]))
    logger.info("* EchoConfig                : "+ str(config_params["ECHOCONFIG"]))
    logger.info("* EchoRecords               : "+ str(config_params["ECHORECORDS"]))

    logger.info("* Logfile                   : "+ str(config_params["LOGGINGFILE"]))
    
    logger.info("***********************************************************")     
    logger.info("")

# end echo_config