
#######################################################################################################################
#
#
#  	Project     	: 	TimeSeries Data generation via Python Application 
#
#   File            :   utils.py
#
#   Description     :   Some common utility functions
#
#                   :   Added ECHOSEEDFILE variable.
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
#   Notes           :   Python Logging Package: 
#                   :   https://docs.python.org/3/library/logging.html
#                   :   https://realpython.com/python-logging/
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "2.0.6.4d"
__copyright__   = "Copyright 2024, - G Leonard"


import logging, os, json, sys


"""
Common Generic Logger setup, used by master loop for console and common file.
"""
def logger(filename, console_debuglevel, file_debuglevel):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(processName)s - %(message)s')

    # create console handler
    ch = logging.StreamHandler()
    
    # Set file log level 
    if console_debuglevel == 0:
        ch.setLevel(logging.DEBUG)
        
    elif console_debuglevel == 1:
        ch.setLevel(logging.INFO)
        
    elif console_debuglevel == 2:
        ch.setLevel(logging.WARNING)
        
    elif console_debuglevel == 3:
        ch.setLevel(logging.ERROR)
      
    elif console_debuglevel == 4:
        ch.setLevel(logging.CRITICAL)
        
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

    # Create a formatter
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(filename)

    # Set file log level 
    if file_debuglevel == 0:
        fh.setLevel(logging.DEBUG)
        
    elif file_debuglevel == 1:
        fh.setLevel(logging.INFO)
        
    elif file_debuglevel == 2:
        fh.setLevel(logging.WARNING)
        
    elif file_debuglevel == 3:
        fh.setLevel(logging.ERROR)
        
    elif file_debuglevel == 4:
        fh.setLevel(logging.CRITICAL)
        
    else:
        fh.setLevel(logging.INFO)  # Default log level if undefined

    fh.setFormatter(file_formatter)
    logger.addHandler(fh)
    
    return logger

# end logger


"""
Common Config Parameters, we want to keep these to the minimum and push site specific config parameters to the seedfile
into the site section.
"""
def configparams():
    
    config_params = {}
    
    # General
    config_params["CONSOLE_DEBUGLEVEL"] = int(os.environ["CONSOLE_DEBUGLEVEL"])
    config_params["FILE_DEBUGLEVEL"]    = int(os.environ["FILE_DEBUGLEVEL"])
    config_params["ECHOSEEDFILE"]       = int(os.environ["ECHOSEEDFILE"])
        
    config_params["LOGGINGFILE"]        = os.environ["LOGGINGFILE"]
    config_params["SEEDFILE"]           = os.environ["SEEDFILE"]
    config_params["SITEIDS"]            = os.environ["SITEIDS"].split(",")
    
    # Mongo
    config_params["MONGO_HOST"]         = os.environ["MONGO_HOST"]
    config_params["MONGO_PORT"]         = os.environ["MONGO_PORT"]
    config_params["MONGO_DIRECT"]       = os.environ["MONGO_DIRECT"]
    config_params["MONGO_ROOT"]         = os.environ["MONGO_ROOT"]
    config_params["MONGO_USERNAME"]     = os.environ["MONGO_USERNAME"]
    config_params["MONGO_PASSWORD"]     = os.environ["MONGO_PASSWORD"]
    config_params["MONGO_DATASTORE"]    = os.environ["MONGO_DATASTORE"]
    config_params["MONGO_COLLECTION"]   = os.environ["MONGO_COLLECTION"]

    config_params["TIMESTAMP_FIELD"]    = os.environ["TIMESTAMP_FIELD"]
    config_params["METADATA_FIELD"]     = os.environ["METADATA_FIELD"]
    config_params["RETENSION_LEVEL"]    = os.environ["RETENSION_LEVEL"]
    
    # Root of file name
    config_params["FILEROOT"]           = os.environ["FILEROOT"]
    
    return config_params

# end configparams


def echo_config(config_params, logger):
    
    
    logger.info("***********************************************************")
    logger.info("* ")
    logger.info("*          Python IoT Sensor data generator")
    logger.info("* ")
    logger.info("***********************************************************")
    logger.info("* General")
    
    logger.info("* Console Debuglevel               : " + str(config_params["CONSOLE_DEBUGLEVEL"])) 
    logger.info("* File Debuglevel                  : " + str(config_params["FILE_DEBUGLEVEL"]))

    logger.info("* Logfile                          : " + config_params["LOGGINGFILE"])
    logger.info("* Seedfile                         : " + config_params["SEEDFILE"])
    logger.info("* Echo Seed File                   : " + str(config_params["ECHOSEEDFILE"]))
    logger.info("* SiteId's                         : " + str(config_params["SITEIDS"]))
    
    # Added in app 4a, improved 4b
    logger.info("* Mongo Host                       : " + config_params["MONGO_HOST"])
    logger.info("* Mongo Port                       : " + config_params["MONGO_PORT"])
    logger.info("* Mongo DataStore                  : " + config_params["MONGO_DATASTORE"])
    logger.info("* Mongo Collection                 : " + config_params["MONGO_COLLECTION"])

    # Added in app4d
    logger.info("* Mongo TS timestamp field         : " + config_params["TIMESTAMP_FIELD"])
    logger.info("* Mongo TS metadata field          : " + config_params["METADATA_FIELD"])
    logger.info("* Mongo TS Resention level field   : " + config_params["RETENSION_LEVEL"])

    # Added in app4c    
    logger.info("* File Root                        : " + config_params["FILEROOT"])
    
    logger.info("***********************************************************")     
    logger.info("")

# end echo_config


# Console print
def pp_json(json_thing, logger, sort=True, indents=4):

    if type(json_thing) is str:
        logger.debug(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))

    else:
        logger.debug(json.dumps(json_thing, sort_keys=sort, indent=indents))

    return None

# end pp_json


""" 
Lets read our entire seed file in.
"""
def read_seed_file(config_params, logger):

    my_seedfile = []
    filename    = config_params["SEEDFILE"]
    
    logger.info('utils.read_seed_file Called ')

    logger.info('utils.read_seed_file Loading Complete Seed file: {file}'.format(
        file=filename
    ))

    try:
        with open(filename, "r") as fh:
            my_seedfile = json.load(fh)


    except IOError as e:
        logger.critical('utils.read_seed_file I/O error: {file}, {errno}, {strerror}"'.format(
            file=filename,
            errno=e.errno,
            strerror=e.strerror
        ), exc_info=True)
        return -1

    except:  # handle other exceptions such as attribute errors
        logger.critical('utils.read_seed_file Unexpected error: {file}, {error}"'.format(
            file=filename,
            error=sys.exc_info()[0]
        ), exc_info=True)
        return -1

    finally:
        fh.close
        logger.info('utils.read_seed_file File Closed')
        
        if config_params["ECHOSEEDFILE"] == 1:
            logger.debug('utils.read_seed_file Printing Complete Seed file')
            pp_json(my_seedfile, logger)
        
        # end if
        
        logger.info('utils.read_seed_file Completed')

        return my_seedfile

    # end try:
# end read_seed_file


"""
Find the specific site in array of sites based on siteId
"""
def find_site(my_seedfile, siteId, logger):
    
    logger.info('utils.find_site Called, SiteId: {siteId}'.format(
        siteId=siteId
    ))

    site    = None
    found   = False

    for site in my_seedfile:
        if site["siteId"] == siteId:
                                                
            logger.info('utils.find_site Retrieved, SiteId: {siteId} '.format(
                siteId=siteId
            ))

            return (site)

    if (found == False):

        logger.critical('utils.find_site Completed, SiteId: {siteId} NOT FOUND '.format(
            siteId=siteId
        ))

        return (-1)

# end find_site
