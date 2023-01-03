# Air Quality on ESP8266
A quick and dirty air quality sensor app for ESP8266, all in Python

Deploy ESP8266 in the field with a CCS811 and a DHT22. It will read temperature, humidity, eCO2, tVOC and send that data back to an API server included here.

# Configurations
There are a few things which will need to be configured for you to run this on your own

## boot.py
In `wlan.connect()`, you will need to update this with your own wlan ssid and passphrase. Optionally, configure an NTP source closer to you for more accurate time, but this probably doesn't really matter. The 8266 drifts a decent bit, its not the most reliable clock.

## main.py
`DATA_URL` : the endpoint hosting your data server to catch the data from your 8266
`LOC` : a location tag, in case you have multiple 8266's going out in the field.

# Running the API
## Basic Info
The API is an extremely basic wsgi application based on falcon. You can use any wsgi runner to run it. If you run the python file directly, it'll use `wsgiref.simple_server` to run on port 8080. You may want to use `gunicorn` or `waitress-serve`, such as `waitress-serve --listen=*.8080 data_receiver.app`.

The API stores all the data in a duckdb database which it will create if it does not already exist. This is a similar database tool to Sqlite.

## API Endpoints
### GET /air_data
Returns an array of samples from the last few days. By default it queries for the last five days, can optionally take a query string param like `?days=10` to get more historical data.

### POST /air_data
Post a single array of samples, in the format `[timestamp, temperature, humidity, eCO2, tVOC, location]`