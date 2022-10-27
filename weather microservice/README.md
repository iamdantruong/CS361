Instructions for Weather Microservice

1. Start weatherApp.py in your console to run the server.
    python weatherApp.py
2. Move send_zip.py to base folder of your python code and import send_zip.py module.
    import send_zip.py
3. Make calls to the server by creating SendZipClient({ZIPCODE}) objects, adding in zip code.
The response will be in JSON format which contains both the name of the city and the temperature.

<br>
To access those values, use the corresponding keys:
<br>
    For city name, use ['name']
<br>
    For temperature, use ['main']['temp']
<br> 
<br>
--------Your code should look like this:---------- 
<br>
rpc = SendZipClient('{ZIPCODE}')            
response = rpc.call()
<br>
city = response['name']
<br>
temperature = response['main]['temp']
<br>

<br> 

If you want to access other values from the response, see below for an example of what
the weather response looks like. <br>
 {   'coord': {'lon': -122.3612, 'lat': 47.3104},  <br>
     'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], <br> 
     'base': 'stations',  <br>
     'main': {'temp': 42.98, 'feels_like': 39.47, 'temp_min': 39.47, 'temp_max': 46.78, 'pressure': 1020, 'humidity': 92}, <br>
     'visibility': 10000, <br>
     'wind': {'speed': 5.75, 'deg': 170}, <br>
     'clouds': {'all': 100}, <br>
     'dt': 1666540663, <br>
     'sys': {'type': 2, 'id': 2012396, 'country': 'US', 'sunrise': 1666535967, 'sunset': 1666573664}, <br>
     'timezone': -25200, <br>
     'id': 5794245, <br>
     'name': 'Federal Way', <br>
     'cod': 200 <br>
     }
<br>
![sequence](./sequence.jpeg)

