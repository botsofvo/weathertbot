from pyowm import OWM
from datetime import datetime

owm = OWM("aa3cc8fac5c1e127a6174ac9b0ef8932")

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
        temp = temperature.get("temp")
        temp_min = temperature.get("temp_min")
        temp_max = temperature.get("temp_max")
        time = timeformater(time)

        results.append("""\n📅 {}\n
        🌏Location : {} 
        🌐lat : {} 
        🌐lon : {} 
        ☔Status: {}
        🍃Detailed: {}
        🌡️Temperature: {}°c
        📉Min temperature: {}°c
        📈Max temperature: {}°c""" .format(time, loc_name, loc_lat, loc_lon, status, detailed, temp, temp_min, temp_max))

    return "\n".join(results[:10])


if __name__ == "__main__":
    print(get_forecasts(-1.2, 36))
