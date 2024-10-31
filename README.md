# Working with MongoDB Timeseries Collections

## Overview

This tutorial, or project (you can decide how you want to view it) will be a series of examples (one building on the next) on how to create timeseries data using a Python application and push it to a MongoDB time Series collection as datastore.

We will build the final application up layer by layer. 

Each new app (layer) will start from where the previous left off and add a new section/functionality
some layers will have a "a", "b", "c" etc. section, where we show different ways to accomplish the same, or a version does the min
to accomplish a task and "b" then improves on it, making it more real world.

## Comments in codde

I will try and springle comments/explanations all through the code, but what might be heavily commented on say in section 2 will have that reduced to the min in section 3, allowing section 3 to rather carry comments pertinant to the secion.


## Timeseries Data

Timeseres Data is the primary data format/structure utilized for IoT data.

It does introduce some concepts that needs to be considered, i.e. every record is primarily comprised out of 3 components.

    - timestamp of the event
    - metadata about the event
        this can be a json document of key/value pairs.
    - measurement/value of the event

This does as such then imply that a timeseries record can not (or should not really) store 2 values.

If multiple values need to be stored they will be seperate records with different metadata tags describing the different measurement being recorded.

## Payload

```		
{
    "timestamp" : "2024-10-02T00:00:00.869Z",
    "metadata" : {
        "siteId" : 1009,
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi"
    },
    "measurement" : 1013.3997
}
```

What follows is multiple Python applications app1 => app5 etc. where we will build up our application (data generator) layer by layer.

    - 1 - app1 - basic environment and logging frame work.
    - 2 - app2 - Read our seed file.
    - 3 - app3 - Generate the timeseries data/payload.
    - 4 - app4 - Push data to MongoDB.
    - 5 - app5 - polish and optimized the stack, i.e. improve logging and then add some timing/instrumention code.


Everything (dependency) that runs locally to simply testing is deployed using a docker-compose.yaml file located in the devlab directory.

These resources can be started by executing make run.

For the MongoDB use MongoDB Compass to create the database and collection or use Mongo sql interface to execute the sql located in the devlab/sql directory. - For this we added code in app4d to auto create the database and collection.


- [MongoDB Timeseries Collection](https://www.mongodb.com/docs/manual/core/timeseries-collections/)


## To run the project.

Each of the applications can be execute by running either the run_x.sh script or by running ```make <appX>``` where X is the application number.

At the correct app number the MongoDB instance will be started as required.

Each of the application directories have a local README.md with additional information about what will be doing/adding.

example:

- make app1         Basic environment variables and logging framework.
- make app2         Read our seed/JSON file. 
- make app3a        The entire Data/payload generation
- make app3b        optimized version, or alternate version accomplising same as app3a
- make app4a        initial version
- make app4b        optimized version, or alternate version accomplising same as app4a, we collapsed the insertOne andInsertMany into one function, insertMongo.
- make app4c        Added write to textfile
- make app4d        Added auto create database and collection
- make app5         Added logging and instrumentation


## Grafana

As per above, we will deploy some Grafana Dashboards to visualize the data.

Note: As the data is stored in a MongoDB Timeseries collection you will require a trial license for Grafana Enterprise.

The Grafana dashboard json code can be found in the grafana folder. Before creating a new dashboard make sure to create the requited datasource.

A non production, single user, test/development license is available for Grafana Enterprise. (A free tier Grafana Cloud account, will allow you to use 1 Enterprise Connector for as long as you want. There's no time limit. ) 

See:

- [Grafana Cloud](https://grafana.com/products/cloud/)

