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
__version__     = "2.0.6.4d"
__copyright__   = "Copyright 2024, - G Leonard"

import bson
import pymongo
import os, json


def createConnectionToStore(config_params, site, mode, logger):
        
    if site["data_persistence"] == 1:   
        return createFileConnection(config_params, site["siteId"], mode, logger)

    else:        
        return createMongoConnection(config_params, site["siteId"], mode, logger)

    # end if
# end createConnectionToStore


def savePayloadToStore(connection, site, mode, payload, logger):
    
    if site["data_persistence"] == 1:
        return writeToFile(connection, site["siteId"], mode, payload, logger)
    
    else:
        return insertMongo(connection, site["siteId"], mode, payload, logger)
        
    # end if
# end savePayloadToStore


def closeConnectionToStore(connection, site, mode, logger):
    
    if site["data_persistence"] == 1:
        closeFileConnection(connection, site["siteId"], mode, logger)
        
    # end if
# end closeConnectionToStore


""" 
Lets create to write json strings to a file.
This will be json structured flattened into a single line.
"""
def createFileConnection(config_params, siteId, mode, logger):
    
    file = None
    
    try:
        filename    = config_params["FILEROOT"] + "_" + str(siteId) + ".json"

        if filename != "": 
            file = open(filename, 'a')  # Open the file in append mode
            
            if file != None:
                logger.debug('connection.createFileConnection - mode {mode} - Filename {filename} OPENED'.format(
                    siteId=siteId,
                    mode=mode,
                    filename=filename
                ))   
                return file

            else:
                return -1
            
            #end if            
        # end if                                 
                       
    except IOError as err:
        logger.critical('connection.createFileConnection - mode {mode} - FAILED Err: {err} '.format(
            siteId=siteId,
            mode=mode,
            err=err
        ))
        
        return -1
    
    # end try
# end createFileConnection


def writeToFile(file, siteId, mode, payload, logger):

    try:

        if file:        
            if mode == 0:
                mode = "writeOne"
                # Convert the payload dictionary to a JSON string
                payload_json = json.dumps(payload)
                file.write(payload_json + '\n')  # Add a newline at the end

            else:

                mode = "writeMany"
                for record in payload:
                    # Convert each payload to a JSON string and write it to the file
                    payload_json = json.dumps(record)
                    file.write(payload_json + '\n')  # Write each payload on a new line
                    
            # end if
                        
            return 1
   
    except IOError as e:
        logger.error('connection.writeToFile - mode {mode} - FAILED, Err: {err}'.format(
            siteId=siteId,
            mode=mode,
            err=e
        ))
        
        return -1

    # end try
# end writeToFile


def closeFileConnection(file, siteId, mode, logger):
    
    if file:
        try:
            file.close()
            
        except IOError as e:
            logger.error('connection.closeFileConnection - mode {mode} - FAILED, Err: {err}'.format(
                siteId=siteId,
                mode=mode,
                err=e
            ))
                        
        # end try
    # endif
# end close_file


def createMongoConnection(config_params, siteId, mode, logger):

    try:
        if config_params["MONGO_USERNAME"] != "": 
            config_params["MONGO_URI"] = f'{config_params["MONGO_ROOT"]}://{config_params["MONGO_USERNAME"]}:{config_params["MONGO_PASSWORD"]}@{config_params["MONGO_HOST"]}:{int(config_params["MONGO_PORT"])}/?{config_params["MONGO_DIRECT"]}'
        
        else:
            config_params["MONGO_URI"] = f'{config_params["MONGO_ROOT"]}://{config_params["MONGO_HOST"]}:{int(config_params["MONGO_PORT"])}/?{config_params["MONGO_DIRECT"]}'
                    
                        
        logger.debug('connection.createMongoConnection - URI: {uri} '.format(
            siteId=siteId,
            uri=config_params["MONGO_URI"]
        ))

        try:
            myclient = pymongo.MongoClient(config_params["MONGO_URI"])
            myclient.server_info()
                                
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logger.critical('connection.createMongoConnection - FAILED Err: {err} '.format(
                siteId=siteId,
                err=err
            ))
            
            return -1
        
        # end try

        # We're going to check of our collection exist... if we're going to create it,
        # If by change our database did not exist either then it will be implicitely also created.
        # if the database did exist then it simply adds the new collection.
        # Normally simply by inserting data into the database/collection would create both, but as we want a timeseries
        # specific collection we need to create it first, as per our configuration requirements.
        try:
            mydb = myclient[config_params["MONGO_DATASTORE"]]
            mydb.validate_collection(config_params["MONGO_COLLECTION"])
            
        except pymongo.errors.OperationFailure:     # If error then either the database or collection does not exist
            logger.critical('connection.createMongoConnection - Datastore {datastore} or Collection {collection} does not exist, CREATING'.format(
                siteId=siteId,
                datastore=config_params["MONGO_DATASTORE"],
                collection=config_params["MONGO_COLLECTION"]
            ))        

            result = create_mongo_ts_collection(mydb, config_params, siteId, logger)
            if result == -1:
                os._exit(-1)

            # end if            
        # end try

        mydb            = myclient[config_params["MONGO_DATASTORE"]]
        my_collection   = mydb[config_params["MONGO_COLLECTION"]]

        logger.info('connection.createMongoConnection - CONNECTED'.format(
            siteId=siteId
        ))
            
        return my_collection
    
    except Exception as e:
        logger.critical('connection.createMongoConnection - FAILED, Err: {err} '.format(
            siteId=siteId,
            err=e
        ))                               

        return -1
    
    # end try
# end createMongoConnection


def insertMongo(collection, siteId, mode, payload, logger):

    try:
        
        if mode == 0:
            mode = "insertOne"
            result = collection.insert_one(payload)

        else:
            mode = "insertMany"
            result = collection.insert_many(payload)
        
        # end if
                     
        return result
   
    except Exception as e:
        logger.error('connection.insertMongo - mode {mode} - FAILED, Err: {err}'.format(
            siteId=siteId,
            mode=mode,
            err=e
        ))
        
        return -1

    # end try
# end insertMongo

def create_mongo_ts_collection(db, config_params, siteId, logger):
    
    try:
        
        time_series_options = {
            "timeField": config_params["TIMESTAMP_FIELD"],      # Field that stores the timestamp
            "metaField": config_params["METADATA_FIELD"],       # Optional: Field to store metadata
            "granularity": config_params["RETENSION_LEVEL"]     # Can be 'seconds', 'minutes', or 'hours'
        }
        
        # Add code to make Collection TS specific.
        db.create_collection(config_params["MONGO_COLLECTION"], timeseries=time_series_options)

        logger.debug('connection.create_ts_collection - Collection {collection}, CREATED'.format(
            siteId=siteId,
            collection=config_params["MONGO_COLLECTION"]
        ))
        return 0
    
    except Exception as e:
        logger.critical('connection.create_mongo_ts_collection - Collection {collection}, Create FAILED, Err: {err}'.format(
            siteId=siteId,
            collection=config_params["MONGO_COLLECTION"],
            err=e
        ))
        
        return -1

    # end try
# end create_ts_collection