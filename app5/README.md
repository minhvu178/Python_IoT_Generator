# Python based IoT SimeSeries data generator

## Overview

At this stage we're polishing the app, This will also be our last "section"

In app5 I'm going to add/change two bits.

- For this last bit I want to address the logging to console and logging to file, optimizing and polishing as I'd like call it... As we've now got a proper view everything, we can see where to modify things to reduce message size andline sizes.

 Previously we included the siteId in the message, which means for every line, printed to file we included "siteId - <siteID>". 
 
 What we did here... We modified the logging formatter to 2 custom formatters, one for console we're now define the logging->processName and set it to siteId, and a seperate one for the file Handler, where we dont include the processName as the file name alreadyed includes the siteId already. This might not seem like much, but as we might be printing the 100 of thousands of records to a file, and every line might include the siteId this could add up...

- I want to add some code to measure time and records processed, aka instrument the code.

### Logging

In utils.py I'm changing logger function. 
I'm creating a console_formatter and file_formatter specific formatter. 


### Instrumentation - Timing.

What we will be doing hre now, We're adding some execution timing to our run_simulation routine. What we will we will basically record the start time and end time of our big loops. Using that we can calculate the execution time.... As we're already recording the number of records, we can also calculate the throughput.

