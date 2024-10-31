# Python based IoT SimeSeries data generator

## Overview
  
In app3a we pretty much created the core/base functionality to be able to create our IoT payloads.

In app3b we stepping up our game a bit as far as simulate.progress_value is concerned.

I want to add a deviation weight to the sensors configuration... 0-10, with 
	5 implying the measurements always circle around mean value, within the sd range, 
	the further above 5 the value is (closer to 10) the further/faster the values climb postive above the mean.
	the lower below 5 the value is (closer to 0) the more/faster it slopes down below the mean.

If Stability factor is less than 50, then the sd will allow values belo min or above max range.

for site level section:
	start_datetime is being renamed to historic_data_start_datetime.
	start_time and end_time is being renamed operational_start_time and operational_end_time.
	We're implying by these that the factory/site only operate/generate data daily between these times.
	If not specfied then data is generated for all 24hours.

for device level section per site the:
	start_time is being renamed to sfd_start_time &
	end_time is being renamed to sfd_end_time.
	sfd implying stability factor deviation. 


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


