# MongoDB - Time Series Collection

# If database does not exist then it's created.
use Mongo0;

# Create tsdb specific collection
db.createCollection("sensor_data", {
  timeseries: {
    timeField:    "timestamp",
    metaField:    "metadata",
    granularity:  "seconds"
  },
  expireAfterSeconds: 86400
});





