#######################################################################################################################
#
#
#  	Project     	    : 	IoT based TimeSeries Data via Python Application 
#
#   File                :   main.py
#
#   Description         :   In this "chapter" we will be reading our entire seedfile: conf/Full2.json in and filter out  
#                           the SiteId's that we want to process. -(these are listed in our environment variable called SITEIDS).
#
#   Created     	    :   19 October 2024
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
__version__     = "2.0.6.2"
__copyright__   = "Copyright 2024, - G Leonard"


import utils, os


config_params   = utils.configparams()
logger          = utils.logger(config_params)

def main():
    
    if config_params["ECHOCONFIG"] == 1: 
        
        utils.echo_config(config_params, logger)
    
    #end if
    
    # Load the Entire SeedFile
    my_seedfile = utils.read_seed_file(config_params["SEEDFILE"], logger, config_params)
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
        utils.pp_json(cur_site)
        my_sites.append(cur_site)

    # end for
# end main

if __name__ == "__main__":

    main()