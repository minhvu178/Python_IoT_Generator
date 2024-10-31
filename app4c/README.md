# Python based IoT SimeSeries data generator

## Overview

At this point, end of app4b we have a python application that generates semi random sensor data based on the parameters defined for the
site/device/sensor.

We can also persist this data to a MongoDB collection.

In 4c we will extend the app to also be capable of writing the data to a text file with each line being a flattened version of our JSON
payload. 

With this addition we're going to go back to simulate.run_simulation => 

	```
		if site["data_persistence"] == 2:
	``` 

	and modify this to be 

	```
		if site["data_persistence"] > 0
	```

if true then we will call a generic save package/function, in which we will then determine the output target and execute according.

Thus moving our create connection and save functions outside the simulate package.


### Our Target payload :
```
	{
		"timestamp" : "2024-10-19T01:00:00.869Z",
		"metadata" : {
			"siteId" : 1009,
			"deviceId" : 1042,
			"sensorId" : 10180,
			"unit" : "Psi"
		},
		"measurement" : 1015.3997
	}
```


