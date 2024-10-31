
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
__version__     = "2.0.6.2"
__copyright__   = "Copyright 2024, - G Leonard"


import logging, os, json, sys
from datetime import datetime


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
    config_params["ECHOSEEDFILE"]   = int(os.environ["ECHOSEEDFILE"])
    config_params["ECHOSITEFILE"]   = int(os.environ["ECHOSITEFILE"])
        
    config_params["LOGGINGFILE"]    = os.environ["LOGGINGFILE"]
    config_params["SEEDFILE"]       = os.environ["SEEDFILE"]
    config_params["SITEIDS"]        = os.environ["SITEIDS"].split(",")
    
    return config_params

# end configparams

def echo_config(config_params, logger):
    
    
    logger.info("***********************************************************")
    logger.info("* ")
    logger.info("*          Python IoT Sensor data generator")
    logger.info("* ")
    logger.info("***********************************************************")
    logger.info("* General")
    
    logger.info("* Debuglevel                : "+ str(config_params["DEBUGLEVEL"]))
    logger.info("* EchoConfig                : "+ str(config_params["ECHOCONFIG"]))
    logger.info("* EchoRecords               : "+ str(config_params["ECHORECORDS"]))
    logger.info("* Echo Seedfile JSON        : "+ str(config_params["ECHOSEEDFILE"]))
    logger.info("* Echo Site definition JSON : "+ str(config_params["ECHOSITEFILE"]))
    
    logger.info("* Logfile                   : "+ str(config_params["LOGGINGFILE"]))
    logger.info("* Seedfile                  : "+ str(config_params["SEEDFILE"]))
    logger.info("* SiteId's                  : "+ str(config_params["SITEIDS"]))
    
    logger.info("***********************************************************")     
    logger.info("")

# end echo_config


def pp_json(json_thing, sort=True, indents=4):

    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))

    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))

    return None

# end pp_json


def read_seed_file(filename, logger, config_params):

    my_seedfile = []
    
    if config_params["DEBUGLEVEL"] >= 1:
        
        logger.info('utils.read_seed_file Called ')

        logger.info('utils.read_seed_file Loading file: {file}'.format(
            file=filename
        ))

    try:
        with open(filename, "r") as fh:
            my_seedfile = json.load(fh)


    except IOError as e:
        logger.error('utils.read_seed_file I/O error: {file}, {errno}, {strerror}"'.format(
            file=filename,
            errno=e.errno,
            strerror=e.strerror
        ))
        return -1

    except:  # handle other exceptions such as attribute errors
        logger.error('utils.read_seed_file Unexpected error: {file}, {error}"'.format(
            file=filename,
            error=sys.exc_info()[0]
        ))
        return -1

    finally:
        fh.close
        if config_params["DEBUGLEVEL"] >= 1:
            logger.info('utils.read_seed_file File Closed ')

        if config_params["ECHOSEEDFILE"] == 1:
            logger.info('utils.read_seed_file Printing Seed file')

            print("------ Seedfile              ------")
            
            pp_json(my_seedfile)

            print("-----------------------------------")

        if config_params["DEBUGLEVEL"] >= 1:
            logger.info('utils.read_seed_file Completed ')

        return my_seedfile

# end read_seed_file


# Find shooter in array of shooters (my_shooter_list) based on siteId
def find_site(my_seedfile, siteId, logger, config_params):
    
    if config_params["DEBUGLEVEL"] >= 2:
        logger.info('utils.find_site Called')

    site    = None
    found   = False

    for site in my_seedfile:
        if site["siteId"] == siteId:

            if config_params["ECHOSITEFILE"] == 1:
                logger.info('utils.find_site Printing, SiteId: {siteId}'.format(
                    siteId=siteId
                ))
                
                pp_json(site)
                
            if config_params["DEBUGLEVEL"] >= 2:
                logger.info('utils.find_site Completed, SiteId: {siteId} '.format(
                    siteId=siteId
                ))

            return (site)

    if (found == False):

        if config_params["DEBUGLEVEL"] >= 2:
            logger.info('utils.find_site Completed, SiteId: {siteId} NOT FOUND '.format(
                siteId=siteId
            ))

        return (-1)

# end find_site