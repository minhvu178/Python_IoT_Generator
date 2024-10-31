
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
__version__     = "2.0.6.3a"
__copyright__   = "Copyright 2024, - G Leonard"


import utils
import time, random
from datetime import datetime, timedelta, timezone
import random


# Function to check if the current time is within the specified time range for the site... to generate events
def is_within_time_range(start_time_str, end_time_str, current_time=None):

    # Convert the string representations of start_time and end_time to datetime objects
    start_time  = datetime.strptime(start_time_str, "%H:%M")
    end_time    = datetime.strptime(end_time_str, "%H:%M")

    if current_time is None:
        current_time = datetime.now()

    return (start_time <= current_time <= end_time)

# end is_within_time_range


# Example function to generate payloads with timezone in the timestamp
def generate_payload(sensor, device, site_id, current_time, time_zone_offset):
    
    # Adjust the timestamp to include the site's local timezone offset
    # Each site is run as if it is running locally in it's own time zone, we simply add the local offset to the payload
    # allowing us to run a single data store in the end, with each timestamp implying it's own UTC offset, thus
    # enabling us to show values across geo locations, but time wise aligned.
    
    offset_hours, offset_minutes    = map(int, time_zone_offset.split(":"))
    tz_offset                       = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
    local_time_with_tz              = current_time.replace(tzinfo=tz_offset)

    # Generate the timestamp with timezone included
    timestamp = local_time_with_tz.isoformat()

    # Generate the sensor measurement, keeping the stabilitty factor in mind and if start_time and end_time is provided
    # for the device, if provided then we scale the sd value used by the stability_factor.
    measurement = progress_value(sensor, device["stabilityFactor"], device, datetime.now())

    # If you want to expand the payload to include more information from our seed file this is where we can do it.
    # Note for Timeseries data paylaod we want to keep it small/compact and to the common accepted 3 values.
    # If we were to push this to a non Timeseries based store/record then well go mad ;)
    
    return {
        "timestamp": timestamp,  # Timestamp now includes the correct timezone
        "metadata": {
            "siteId": site_id,
            "deviceId": device["deviceId"],
            "sensorId": sensor["sensorId"],
            "unit": sensor["unit"]
        },
        "measurement": measurement
    }

# end generate_payload


def progress_value(sensor, stability_factor, device, current_time, method="normal"):
    
    """
    Generate a sensor value, 
    Scaling sd based on stability_factor if the current time is within device start_time and end_time.
    If start_time and end_time are not provided for the device, no scaling is applied.
    """
    
    sd      = sensor["sd"]
    mean    = sensor["mean"]

    # Check if device has start_time and end_time, and scale sd only if they are provided
    if "start_time" in device and "end_time" in device:
        
        device_start_time   = datetime.strptime(device["start_time"], "%H:%M")
        device_end_time     = datetime.strptime(device["end_time"], "%H:%M")
        current_time_local  = current_time.time()  # We only care about the time portion
        
        if device_start_time.time() <= current_time_local <= device_end_time.time():
            # Scale standard deviation if within the specified time range
            sd = sd * (100 - stability_factor) / 100

    # Generate sensor value using normal or uniform distribution
    if method == "normal":
        
        return round(random.gauss(mean, sd), 4)
    
    elif method == "uniform":
        lower_bound = max(0, mean - sd)
        upper_bound = mean + sd
        
        return round(random.uniform(lower_bound, upper_bound), 4)

# end progress_value


""" 
Function to run simulation for a specific site
"""
def run_simulation(site, current_time, config_params):

    # Create new site specific logger's
    logger = utils.logger(config_params["LOGGINGFILE"] + "_" + str(site["siteId"]) + ".log", site["console_debuglevel"], site["file_debuglevel"])
        
    logger.info("simulate.run_simulation - Site ID {siteId}: Starting simulation".format(
        siteId=site["siteId"]
    ))
    
    logger.debug('simulate.run_simulation - Site ID {siteId}: Printing Complete site record')
    utils.pp_json(site, logger)
    
    # Site's time zone offset (e.g., "+2:00")
    site_time_zone = site.get("time_zone", site["time_zone"])
        
    # Parse the start_datetime and begin simulation
    if "start_datetime" in site and site["start_datetime"]:
        oldest_time = datetime.strptime(site["start_datetime"], "%Y-%m-%dT%H:%M")
        
    else:
        oldest_time = current_time

    # Determine time range for simulation, if we specify this then the site/device/sensor only create measurements
    # ... within the specified time range, otherwise we run the simulation for the full day range/24 hours.
    run_limited_time = "start_time" in site and "end_time" in site
    if run_limited_time:
        start_time  = site["start_time"]
        end_time    = site["end_time"]

    # Historical phase
    if "start_datetime" in site and site["start_datetime"]:
                
        logger.info("simulate.run_simulation - Site ID {siteId}: Running historical phase starting from {start_datetime}".format(
            siteId=site["siteId"],
            start_datetime=site["start_datetime"]
        ))
    
        
        while oldest_time < current_time:
            if run_limited_time:
                if not is_within_time_range(start_time, end_time, oldest_time):
                    oldest_time += timedelta(milliseconds=site["sleeptime"])  # Skip out-of-range times
                    continue

            for device in site["devices"]:
                for sensor in device["sensors"]:
                    payload = generate_payload(sensor, device, site["siteId"], oldest_time, site_time_zone)
                                        
                    logger.debug("simulate.run_simulation - Hist Ph: Payload {payload}".format(
                        siteId=site["siteId"],
                        payload=payload
                    ))
                    
                    sensor["last_value"] = payload["measurement"]

            oldest_time += timedelta(milliseconds=site["sleeptime"])

        logger.info("simulate.run_simulation - Site ID {siteId}: Completed historical phase starting from {start_datetime}".format(
            siteId=site["siteId"],
            start_datetime=site["start_datetime"]
        ))     

    # end Historical phase


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

            for device in site["devices"]:
                for sensor in device["sensors"]:
                    payload = generate_payload(sensor, device, site["siteId"], current_loop_time, site_time_zone)
                    
                    logger.debug("simulate.run_simulation - Cur Ph: Payload {payload}".format(
                        siteId=site["siteId"],
                        payload=payload
                    ))
                    sensor["last_value"] = payload["measurement"]

            time.sleep(site["sleeptime"] / 1000)  # Convert milliseconds to seconds

        logger.info("simulate.run_simulation - Site ID {siteId}: Completed current phase".format(
            siteId=site["siteId"]
        ))
        
    logger.info("simulate.run_simulation - Site ID {siteId}: Completed simulation".format(
        siteId=site["siteId"]
    ))

# end run_simulation