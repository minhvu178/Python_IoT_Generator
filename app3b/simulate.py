
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
__version__     = "2.0.6.3b"
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
def generate_payload(site, device, sensor, current_time, time_zone_offset):
    
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
    measurement = progress_value(sensor, current_time, device["sfd_start_time"], device["sfd_end_time"], device["stabilityFactor"])

    # If you want to expand the payload to include more information from our seed file this is where we can do it.
    # Note for Timeseries data paylaod we want to keep it small/compact and to the common accepted 3 values.
    # If we were to push this to a non Timeseries based store/record then well go mad ;)
    
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
Progress the sensor value based on the current time and the configuration settings.
"""
def progress_value(sensor, current_time_local, sfd_start_time_str, sfd_end_time_str, stabilityFactor):

    # Convert string time to datetime.time
    sfd_start_time = datetime.strptime(sfd_start_time_str, "%H:%M").time()
    sfd_end_time = datetime.strptime(sfd_end_time_str, "%H:%M").time()

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
    if "historic_data_start_datetime" in site and site["historic_data_start_datetime"]:
        oldest_time = datetime.strptime(site["historic_data_start_datetime"], "%Y-%m-%dT%H:%M")
        
    else:
        oldest_time = current_time

    # end if
    
    # Determine time range for simulation, if we specify this then the site/device/sensor only create measurements
    # ... within the specified time range, otherwise we run the simulation for the full day range/24 hours.
    run_limited_time = "operational_start_time" in site and "operational_end_time" in site
    if run_limited_time:
        
        start_time  = site["operational_start_time"]
        end_time    = site["operational_end_time"]

    # en dif
    
    # Historical phase
    if "historic_data_start_datetime" in site and site["historic_data_start_datetime"]:
                
        logger.info("simulate.run_simulation - Site ID {siteId}: Running historical phase starting from {historic_data_start_datetime}".format(
            siteId=site["siteId"],
            historic_data_start_datetime=site["historic_data_start_datetime"]
        ))
    
        
        while oldest_time < current_time:
            if run_limited_time:
                if not is_within_time_range(start_time, end_time, oldest_time):
                    oldest_time += timedelta(milliseconds=site["sleeptime"])  # Skip out-of-range times
                    continue
                # end if
            # end if
            
            for device in site["devices"]:
                for sensor in device["sensors"]:
                    
                    payload = generate_payload(site, device, sensor, oldest_time, site_time_zone)
                                        
                    logger.debug("simulate.run_simulation - Hist Ph: Payload {payload}".format(
                        siteId=site["siteId"],
                        payload=payload
                    ))
                    
                    sensor["last_value"] = payload["measurement"]
                # end for
            # end for
    
            oldest_time += timedelta(milliseconds=site["sleeptime"])
        # end while
    
        logger.info("simulate.run_simulation - Site ID {siteId}: Completed historical phase starting from {historic_data_start_datetime}".format(
            siteId=site["siteId"],
            historic_data_start_datetime=site["historic_data_start_datetime"]
        ))  
           
    # end if
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
                
                # end if
            # end if
            
            for device in site["devices"]:
                for sensor in device["sensors"]:
                    
                    payload = generate_payload(site, device, sensor, current_loop_time, site_time_zone)
                    
                    logger.debug("simulate.run_simulation - Cur Ph: Payload {payload}".format(
                        siteId=site["siteId"],
                        payload=payload
                    ))
                    sensor["last_value"] = payload["measurement"]

                # end for
            # end for
            time.sleep(site["sleeptime"] / 1000)  # Convert milliseconds to seconds

        # end for

        logger.info("simulate.run_simulation - Site ID {siteId}: Completed current phase".format(
            siteId=site["siteId"]
        ))
        
    # end if
    # end Current phase
    
    logger.info("simulate.run_simulation - Site ID {siteId}: Completed simulation".format(
        siteId=site["siteId"]
    ))

# end run_simulation