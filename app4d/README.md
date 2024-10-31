# Python based IoT SimeSeries data generator

## Overview

We now have everything we really need, to generate some IoT SimeSeries data and persist it into a datastore. At this stage we're pretty much just doing polishing, adding bits to improve the entire stack.

In app4d I'm going to add/change two bits.

- I want to up the game for our MongoDB interfacing. In appd4/connection.py in the createConnectionToStore() function:


## MongoDB Interfacing

### Create database

We will modify to first check if the database exists, if not create it.

	- How we accomplish this is by simply calling our Timeseries create function to create our timeseries specific collection, which implicitely also creates our database.

### Create collection

We will modify the code to confirm if the collection exists, if not, lets create it, this assumes our database already excisted.

	- For the collection create I've added create_ts_collection.


