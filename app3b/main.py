#######################################################################################################################
#
#
#  	Project     	    : 	IoT based TimeSeries Data via Python Application 
#
#   File                :   main.py
#
#   Description         :   In app3a we pretty much created the core/base functionality to be able to create our IoT payloads.
#                       :   In app3b we stepping up our game a bit as far as simulate.progress_value is concerned.
#
#                       :   I want to add a deviation weight to the sensors configuration... 0-10, with 
#                       :       5 implying the measurements always circle around mean value, within the sd range, 
#                       :       the further above 5 the value is (closer to 10) the further/faster the values climb postive above the mean.
#                       :       the lower below 5 the value is (closer to 0) the more/faster it slopes down below the mean.
#
#                       :   If Stability factor is less than 50, then the sd will allow values belo min or above max range.
#
#                       :   for site level section:
#                       :       start_datetime is being renamed to historic_data_start_datetime.
#                       :       start_time and end_time is being renamed operational_start_time and operational_end_time.
#                       :       We're implying by these that the factory/site only operate/generate data daily between these times.
#                       :       If not specfied then data is generated for all 24hours.
#
#                       :   for device level section per site the:
#                       :       start_time is being renamed to sfd_start_time &
#                       :       end_time is being renamed to sfd_end_time.
#                       :       sfd implying stability factor deviation.            
#
#   Created     	    :   18 October 2024
#
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
__version__     = "2.0.6.3b"
__copyright__   = "Copyright 2024, - G Leonard"


import utils, simulate
import os, multiprocessing
from datetime import datetime
import multiprocessing



def main():
        
    runTime                      = str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    config_params                = utils.configparams()
    config_params["LOGGINGFILE"] = config_params["LOGGINGFILE"] + "_" + runTime
    logger                       = utils.logger(config_params["LOGGINGFILE"] + "_common.log", config_params["CONSOLE_DEBUGLEVEL"], config_params["FILE_DEBUGLEVEL"])

    logger.info("STARTING run, logfile => {logfile}".format(
        logfile=config_params["LOGGINGFILE"]
    ))
    
    
    utils.echo_config(config_params, logger)
        
        
    # Load the Entire SeedFile
    my_seedfile = utils.read_seed_file(config_params["SEEDFILE"], logger)
    if my_seedfile == -1 :
        os._exit(1)
        
    # end if
    

    # Load/filter out the site data based on SITESIDS environment variable.
    my_sites = []
    for siteId in config_params["SITEIDS"]:
        
        cur_site = utils.find_site(my_seedfile, int(siteId), logger)
        if cur_site == -1:
            os._exit(1)
                    
        # end if
        my_sites.append(cur_site)
    # end for
    
    logger.debug("main.main Printing Configuration of selected sites extracted from Seedfile {seedfile}".format(
        seedfile=config_params["SEEDFILE"]
    ))
    
    # pp_json only prints during debug level due to the volume of information
    utils.pp_json(my_sites, logger)
        
    current_time = datetime.now()
    
    # Create processes for each site
    processes = []
    for site in my_sites:
        logger.info("Calling simulate.run_simulation for SiteId {siteId}".format(
            siteId=site["siteId"]
        ))
        
        # Create a process for each site
        p = multiprocessing.Process(target=simulate.run_simulation, args=(site, current_time, config_params))
        processes.append(p)
        p.start()

    # end for
    
    for p in processes:
        p.join()
        
    # end for
        
    logger.info("COMPLETED run, logfile => {logfile}".format(
        logfile=config_params["LOGGINGFILE"]
    ))
    
# end main

if __name__ == "__main__":

    main()