#######################################################################################################################
#
#
#  	Project     	: 	TimeSeries Data generation via Python Application 
#
#   File            :   connection.py
#
#   Description     :   Functions that we will use to persist the data to file and MongoDB Atlas
#
#                   :   Options:
#                   :       - site["data_persistence"] = 0 => None
#                   :       - site["data_persistence"] = 1 => File
#                   :       - site["data_persistence"] = 2 => MongoDB Atlas
#
#   Created     	:   21 October 2024
#
#   Changelog       :   See bottom
#
#   JSON Viewer     :   https://jsonviewer.stack.hu
#
#   Mongodb         :   https://www.mongodb.com/cloud/atlas      
#                   :   https://hub.docker.com/r/mongodb/mongodb-atlas-local
#
#   Notes           :   
#
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "2.0.6.4b"
__copyright__   = "Copyright 2024, - G Leonard"

import bson
import pymongo
import os


def createMongoConnection(config_params, siteId, logger):

    try:
        if config_params["MONGO_USERNAME"] != "": 
            config_params["MONGO_URI"] = f'{config_params["MONGO_ROOT"]}://{config_params["MONGO_USERNAME"]}:{config_params["MONGO_PASSWORD"]}@{config_params["MONGO_HOST"]}:{int(config_params["MONGO_PORT"])}/?{config_params["MONGO_DIRECT"]}'
        
        else:
            config_params["MONGO_URI"] = f'{config_params["MONGO_ROOT"]}://{config_params["MONGO_HOST"]}:{int(config_params["MONGO_PORT"])}/?{config_params["MONGO_DIRECT"]}'
                    
                        
        logger.debug('connection.createMongoConnection - Site ID {siteId} - URI: {uri} '.format(
            siteId=siteId,
            uri=config_params["MONGO_URI"]
        ))

        try:
            myclient = pymongo.MongoClient(config_params["MONGO_URI"])
            myclient.server_info() # force connection on a request as the
                                # connect=True parameter of MongoClient seems
                                # to be useless here 
                                
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logger.critical('connection.createMongoConnection - Site ID {siteId} - FAILED Err: {err} '.format(
                siteId=siteId,
                err=err
            ))
            
            return -1
        
        # end try
                    
        mydb            = myclient[config_params["MONGO_DATASTORE"]]
        my_collection   = mydb[config_params["MONGO_COLLECTION"]]
        
        logger.info('connection.createMongoConnection - Site ID {siteId} - CONNECTED'.format(
            siteId=siteId
        ))
            
        return my_collection
    
    except Exception as e:
        logger.critical('connection.createMongoConnection - Site ID {siteId} - FAILED, Err: {err} '.format(
            siteId=siteId,
            err=e
        ))                               

        return -1
    
    # end try
# end createMongoConnection


def insertMongo(mongodb_collection, siteId, mode, payload, logger):

    try:
        
        if mode == 1:
            mode = "insertOne"
            result = mongodb_collection.insert_one(payload)

        else:
            mode = "insertMany"
            result = mongodb_collection.insert_many(payload)
        
        # end if
                     
        return result
   
    except Exception as e:
        logger.error('connection.insertMongo - Site ID {siteId}, mode {mode} - FAILED, Err: {err}'.format(
            siteId=siteId,
            mode=mode,
            err=e
        ))
        
        return -1

    # end try
# end insertMongo

