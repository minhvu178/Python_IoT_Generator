
#######################################################################################################################
#
#
#  	Project     	: 	TimeSeries Data generation via Python Application 
#
#   File            :   simulate.py
#
#   Description     :   Data simulator/creator
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
#   Notes           :   Python Logging Package: 
#                   :   https://docs.python.org/3/library/logging.html
#                   :   https://realpython.com/python-logging/
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "2.0.6.4a"
__copyright__   = "Copyright 2024, - G Leonard"


import utils, connection
import time, random, os, json
from datetime import datetime, timedelta, timezone
import random


# Function to check if the current time is within the specified time range for the site
# Business/operational hours or 24 hour site
def is_within_time_range(start_time_str, end_time_str, current_time=None):
    
    # Convert the string representations of start_time and end_time to time objects
    start_time  = datetime.strptime(start_time_str, "%H:%M").time()
    end_time    = datetime.strptime(end_time_str, "%H:%M").time()

    # just make sure we're not comparing against Null.
    if current_time is None:
        current_time = datetime.now().time()  # Get only the time part
    else:
        current_time = current_time.time()  # Ensure current_time is a time object

    # end if

    # Check if the current time is within the specified time range
    if start_time < end_time:   # Return true... we're suppose to work/generate data between these times
        return start_time <= current_time <= end_time
    
    else:  # Check if end_time is less than start_time, meaning the time range spans midnight
        return current_time >= start_time or current_time <= end_time

    # end if
    return False    # Should never get here, but just in case

# end is_within_time_range


# Helper to convert local time with timezone to UTC
def convert_to_utc(local_time_with_tz):
    return local_time_with_tz.astimezone(timezone.utc)


# Example function to generate payloads with timezone in the timestamp
def generate_payload(site, device, sensor, current_time, time_zone_offset):
        
   # Adjust the timestamp to include the site's local timezone offset
    offset_hours, offset_minutes = map(int, time_zone_offset.split(":"))
    tz_offset                    = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
    local_time_with_tz           = current_time.replace(tzinfo=tz_offset)

    # Convert the local time to UTC for MongoDB storage
    timestamp = convert_to_utc(local_time_with_tz)

    measurement = progress_value(sensor, current_time, device["sfd_start_time"], device["sfd_end_time"], device["stabilityFactor"])
    
    return {
        "timestamp": timestamp,  # Timestamp now includes the correct timezone
        "metadata": {
            "siteId": site["siteId"],
            "deviceId": device["deviceId"],
            "sensorId": sensor["sensorId"],
            "unit": sensor["unit"]
        },
        "measurement": measurement
    }

# end generate_payload


"""
Generate a sensor value, 
Scaling sd based on stability_factor if the current time is within device start_time and end_time.
If start_time and end_time are not provided for the device, no scaling is applied.
"""
def progress_value(sensor, current_time_local, sfd_start_time_str, sfd_end_time_str, stabilityFactor):
 
    # Convert string time to datetime.time
    sfd_start_time  = datetime.strptime(sfd_start_time_str, "%H:%M").time()
    sfd_end_time    = datetime.strptime(sfd_end_time_str, "%H:%M").time()

    # Ensure current_time_local is a time object
    current_time_local_time = current_time_local.time()

    # Proceed only if the current time is within the specified range
    if sfd_start_time <= current_time_local_time <= sfd_end_time:

        # Calculate the sensor value based on deviation_weight and stabilityFactor
        mean             = sensor['mean']
        sd               = sensor['sd']
        min_value        = sensor['min_range']
        max_value        = sensor['max_range']
        deviation_weight = sensor.get('deviation_weight', 5)  # Default to 5 if not specified
        
        # Adjust mean based on deviation_weight
        if deviation_weight == 5:
            new_mean = mean
            
        elif deviation_weight > 5:
            weight_factor = (deviation_weight - 5) / 5.0  # Scale between 0 and 1
            new_mean = mean + weight_factor * (max_value - mean)
            
        else:
            weight_factor = (5 - deviation_weight) / 5.0  # Scale between 0 and 1
            new_mean = mean - weight_factor * (mean - min_value)

        # end if
        
        # Adjust for stabilityFactor < 50
        if stabilityFactor < 50:
            if deviation_weight > 7:
                new_mean = min(new_mean, max_value + (deviation_weight - 7) * sd)
                
            elif deviation_weight < 3:
                new_mean = max(new_mean, min_value - (3 - deviation_weight) * sd)

            # end if
        # end if
        
        # Generate value based on the new mean and sd
        value = random.gauss(new_mean, sd)

        # Clamp the value to be within the min and max range
        value = max(min_value, min(value, max_value))

        return value
    else:
        # Return the default mean if outside the time range
        return sensor['mean']

    # end if
# end progress_value


""" 
Function to run simulation for a specific site, this is main body of the generator
"""
def run_simulation(site, current_time, config_params):

    
    # Create new site specific logger's
    logger = utils.logger(config_params["LOGGINGFILE"] + "_" + str(site["siteId"]) + ".log", site["console_debuglevel"], site["file_debuglevel"])
        
    logger.info("simulate.run_simulation - Site ID {siteId}: Starting simulation".format(
        siteId=site["siteId"]
    ))
    
    logger.debug('simulate.run_simulation - Site ID {siteId}: Printing Complete site record'.format(
        siteId=site["siteId"]
    ))   
    utils.pp_json(site, logger)
    
    site_time_zone = site["time_zone"]
        
    # Parse the start_datetime and begin simulation
    if "historic_data_start_datetime" in site and site["historic_data_start_datetime"]:
        oldest_time = datetime.strptime(site["historic_data_start_datetime"], "%Y-%m-%dT%H:%M")
        
    else:
        oldest_time = current_time

    # Determine time range for simulation, if we specify this then the site/device/sensor only create measurements
    # ... within the specified time range, otherwise we run the simulation for the full day range/24 hours.

    run_limited_time = False        
    if "operational_start_time" in site and "operational_end_time" in site:
        run_limited_time = True
        
        start_time  = site["operational_start_time"]
        end_time    = site["operational_end_time"]
        
    # end if


    batch_flush_counter         = 0
    historical_record_counter   = 0
    current_record_counter      = 0
    total_record_counter        = 0
    # File based persistence



    # MongoDB persistence
    if site["data_persistence"] == 2:
        flush_size      = site["flush_size"]

        if flush_size > 1:
            mydocs = []
            mode = 2        # InsertMany

        else:
            mode = 1        # InsertOne

        # end if
        
        mongodb_collection = connection.createMongoConnection(config_params, site["siteId"], logger)        
        
        if mongodb_collection == -1:
            logger.critical("simulate.run_simulation - Site ID {siteId}: EXITING".format(
                siteId=site["siteId"]
            ))
            
            os._exit(1)

        # end if
    # end if
    
    
    # Historical phase
    if "historic_data_start_datetime" in site and site["historic_data_start_datetime"]:
                
        logger.info("simulate.run_simulation - Site ID {siteId}: Running historical phase starting from {historic_data_start_datetime}".format(
            siteId=site["siteId"],
            historic_data_start_datetime=site["historic_data_start_datetime"]
        ))
    
        
        while oldest_time < current_time:
            
            # chec if we're specified a start end day for day
            if run_limited_time:
                if not is_within_time_range(start_time, end_time, oldest_time):
                    oldest_time += timedelta(milliseconds=site["sleeptime"])
                    continue
                
                    print("Skipping record outside time range, this should never happen/print")
                # end if
            # end if
            
            for device in site["devices"]:
                for sensor in device["sensors"]:
                    
                    payload = generate_payload(site, device, sensor, oldest_time, site_time_zone)
                    batch_flush_counter += 1
                    historical_record_counter += 1
                    total_record_counter += 1
                    
                    if site["data_persistence"] == 2:
                        if mode == 1:
                            result              = connection.insertOne(mongodb_collection, site["siteId"], payload, logger)
                            batch_flush_counter = 0
                            
                        else: # mode=2
                            mydocs.append(payload)
                        
                            if batch_flush_counter==flush_size:
                                # Post to MongoDB
                                result = connection.insertMany(mongodb_collection, site["siteId"], mydocs, logger)
                                
                                logger.debug("  Flushing/Adding {batch_flush_counter} to {total_record_counter}".format(
                                    batch_flush_counter=batch_flush_counter,
                                    total_record_counter=total_record_counter
                                ))

                                # Reset Flush (recs_processed) Counter
                                batch_flush_counter  = 0
                                mydocs               = []
                                        
                            # end if
                        # end if
                    # end if
                                                            
                    logger.debug("simulate.run_simulation - Hist Ph: Payload {payload}".format(
                        payload=payload
                    ))
                    
                    sensor["last_value"] = payload["measurement"]
                
                # end for
            # end for
            
            oldest_time += timedelta(milliseconds=site["sleeptime"])

        # end while
    
    
        # Post last batch of records in our mydocs variable to MongoDB
        if site["data_persistence"] == 2 and mode == 2 and batch_flush_counter > 0 :
            result = connection.insertMongo(mongodb_collection, site["siteId"], mode, mydocs, logger)
            
            logger.debug("  Flushing/Adding {batch_flush_counter} to {total_record_counter}".format(
                batch_flush_counter=batch_flush_counter,
                total_record_counter=total_record_counter
            ))
        # end if
        
        logger.info("simulate.run_simulation - Site ID {siteId}: Completed historical phase starting from {historic_data_start_datetime}, {historical_record_counter} records".format(
            siteId=site["siteId"],
            historic_data_start_datetime=site["historic_data_start_datetime"],
            historical_record_counter=historical_record_counter
        ))    

    # end Historical phase


    if site["data_persistence"] == 2:
        batch_flush_counter  = 0
        mydocs               = []

    # end if
    
    # Current phase    
    if site["reccap"] > 0:
        logger.info("simulate.run_simulation - Site ID {siteId}: Running current phase".format(
            siteId=site["siteId"]
        ))
        
        for loop in range(site["reccap"]):
            current_loop_time = oldest_time + timedelta(milliseconds=site["sleeptime"] * loop)

            if run_limited_time:
                if not is_within_time_range(start_time, end_time, current_loop_time):
                    continue

                # end if
            # end if
            
            for device in site["devices"]:
                for sensor in device["sensors"]:
                    
                    payload = generate_payload(site, device, sensor, current_loop_time, site_time_zone)
                    batch_flush_counter += 1
                    current_record_counter += 1
                    total_record_counter += 1

                    if site["data_persistence"] == 2:
                        if mode == 1:
                            result = connection.insertMongo(mongodb_collection, site["siteId"], mode, payload, logger)
                            batch_flush_counter = 0
                            
                        else:
                            mydocs.append(payload)
                        
                            if batch_flush_counter==flush_size:
                                # Post to MongoDB
                                result = connection.insertMongo(mongodb_collection, site["siteId"], mode, mydocs, logger)
                                
                                logger.debug("  Flushing/Adding {batch_flush_counter} to {current_record_counter}".format(
                                    batch_flush_counter=batch_flush_counter,
                                    current_record_counter=current_record_counter
                                ))

                                # Reset Flush (recs_processed) Counter
                                batch_flush_counter  = 0
                                mydocs               = []
                                
                            # end if
                        # end if
                    # end if
                    
                    logger.debug("simulate.run_simulation - Cur Ph: Payload {payload}".format(
                        payload=payload
                    ))
                    sensor["last_value"] = payload["measurement"]
                    
                # end for
            # end for
            time.sleep(site["sleeptime"] / 1000)  # Convert milliseconds to seconds
            logger.debug("simulate.run_simulation - Cur Ph: Current Record {current_record_counter}".format(
                current_record_counter=current_record_counter
            ))
        # end for
        

       # Post last batch of records in our mydocs variable to MongoDB
        if site["data_persistence"] == 2 and mode == 2 and batch_flush_counter > 0 :
            result = connection.insertMongo(mongodb_collection, site["siteId"], mode, mydocs, logger)
            
            logger.debug("  Flushing/Adding {batch_flush_counter} to {current_record_counter}".format(
                batch_flush_counter=batch_flush_counter,
                current_record_counter=current_record_counter
            ))
                
        # end if

        logger.info("simulate.run_simulation - Site ID {siteId}: Completed current phase, {current_record_counter} records".format(
            siteId=site["siteId"],
            current_record_counter=current_record_counter
        )) 

    # end if
    
    logger.info("simulate.run_simulation - Site ID {siteId}: Completed simulation: {historical_record_counter} + {current_record_counter} => {total_record_counter} records".format(
        siteId=site["siteId"],
        historical_record_counter=historical_record_counter,
        current_record_counter=current_record_counter,
        total_record_counter=total_record_counter

    ))

# end run_simulation