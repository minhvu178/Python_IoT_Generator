# Python based IoT SimeSeries data generator

## Overview

In this version we will show how to read our json configuration file in and store it's contents in a variable (my_seedfile) over which we can then iterate, or access individual specific sections. We will further loop through out SITEIDS variable and search for the listed sites and print them.

The printing of the entire seed file or the individual site records are controlled by the ECHOSEEDFILE and ECHOSITEFILE config parameters.

## Seed Data

The file basically lists our sites, the devices per site and the sensors per device. Depending on the device it will define the sensors fitted.

### Sites

Our file is an array of json documents, the first level document is our sites.

For each site we provide: 

- siteId
- name
- location (lat, long).

### Devices

Next we provide an array (list) of devices, for each device will be a document comprised out of:

- deviceId
- deviceType (We have various types pumps, motors and ovens)
- stabilityFactor, the lower the worse performing the device is, we will also cause more deviation from mean, based on expected sd the lower the number is.
- start_time, if it has a low stabilityFactor this implies when the sensors on the device will start misbehaving
- end_time, when it will magically start performing back inside it's min/max and close to the mean value, inside the sd range.
- sensors are also an array (list) of documents, each document being a sensor. 

### Sensors

- sensorId
- min_range
- max_range
- unit
- sensorType
- sd
- mean


## Type of Devices 

So we have a couple of different devices each with specific set sensors attached, at minimum.

- Oil Pumps
    We will measure at min always have, pressure sensor, temperature sensor, (current sensor and voltage sensor or Revolutions)

- Fuel Pumps
    We will measure at min always have, pressure sensor, temperature sensor, (current sensor and voltage sensor or revolution and flow_rate sensor)

- Water Pumps
    We will measure at min always have, pressure sensor, revolution sensor and/or flow_rate sensor.

- Hoist Motors
    We will measure at min always have, temperature sensor, current sensor and voltage sensor, revolutions sensor

- Conveyer Motors
    We will measure at min always have, temperature sensor, current sensor and voltage sensor, revolutions sensor,

- Gas Oven
    We will measure at min always have, temperature sensor, fuel_rate sensor

- Pressure Oven
    We will measure at min always have, pressure sensor, temperature sensor, current sensor and voltage sensor
