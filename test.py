from pyowm import OWM
import os
from datetime import datetime
# from dotenv import load_dotenv

# load_dotenv()

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
    current_loc=f"<br>🛩️<b>Your current location information:</b> <br><img src='https://source.unsplash.com/300x200/?{loc_name}' alt='city'><br> 🌏Location : {loc_name}<br> 🌐latitude : {loc_lat} <br> 🌐longitude : {loc_lon} <br>"
    results = []

    for forecast in forecasts:
        time = forecast.reference_time("iso")
        status = forecast.status
        detailed = forecast.detailed_status
        humidity = forecast.humidity
        wind=forecast.wind(unit='miles_hour')
        wind_speed=wind.get("speed")
        temperature = forecast.temperature("celsius")
        # temp = temperature.get("temp")
        temp_min = temperature.get("temp_min")
        temp_max = temperature.get("temp_max")
        time = timeformater(time)
        results.append("""<br><p><img src='https://source.unsplash.com/700x600/?{}' alt='weather'></p>
        📅 <b>{}</b>
        <br>
        <b>🌄Status:</b> {}
        <br>
        <b>☁️Detailed:</b> {}
        <br>
        <b>🌫️humidity:</b> {}%
        <br>
        <b>📉Min temperature:</b> {}°C
        <br>
        <b>📈Max temperature:</b> {}°C
        <br>
        <b>🍃wind speed:</b><br> {} miles/hour""" .format(''.join(detailed), time, status, detailed,humidity, temp_min, temp_max, wind_speed))

    return (current_loc+"<br><b>24 hour forecast:</b><br>"+"<br>".join(results[:10]))

if __name__=="__main__":
    c=get_forecasts(51.5098,-0.1180)
    print(c)
