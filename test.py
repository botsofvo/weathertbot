from pyowm import OWM
import os
from datetime import datetime

owm = OWM(os.getenv('OWM_API_KEY'))

mgr = owm.weather_manager()


def timeformater(time):
    datetime_list = time.split(' ')
    date = datetime_list[0]
    time = datetime_list[1]
    hour = time.split(":")
    hour = hour[0]+":"+hour[1]
    current_time = datetime.strptime(hour, "%H:%M")
    return "Date: "+date+"\n🕒 Time: "+str(current_time.strftime("%I:%M %p"))


def get_forecasts(lat, lon):
    observation = mgr.forecast_at_coords(lat, lon, "3h")
    forecasts = observation.forecast
    location = forecasts.location
    loc_name = location.name
    loc_lat = location.lat
    loc_lon = location.lon
    results = []

    for forecast in forecasts:
        time = forecast.reference_time("iso")
        status = forecast.status
        detailed = forecast.detailed_status
        temperature = forecast.temperature("celsius")
        # temp = temperature.get("temp")
        temp_min = temperature.get("temp_min")
        temp_max = temperature.get("temp_max")
        time = timeformater(time)
        current_loc=f"<br>🛩️<b>Your current location information:</b> <br><br> 🌏Location : {loc_name} <br> 🌐latitude : {loc_lat} <br> 🌐longitude : {loc_lon} <br>"

        results.append("""<br>📅 {}<br>
        ☔Status: {} <br>
        ☁️Detailed: {} <br>
        📉Min temperature: {}°C <br>
        📈Max temperature: {}°C <br>""" .format(time, status, detailed, temp_min, temp_max))

    return current_loc+"<br><b>24 hour forecast:</b><br>"+"<br>".join(results[:10])
