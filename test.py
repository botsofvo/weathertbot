from pyowm import OWM

owm =OWM("aa3cc8fac5c1e127a6174ac9b0ef8932")

mgr = owm.weather_manager()

def get_forecasts(lat, lon):
    observation = mgr.forecast_at_coords(lat, lon, "3h")
    forecasts = observation.forecast

    location = forecasts.location
    loc_name = location.name
    loc_lat = location.lat
    loc_lon = location.lon

    results= []

    for forecast in forecasts:
        time = forecast.reference_time("iso")
        status = forecast.status
        detailed = forecast.detailed_status
        temperature = forecast.temperature("celsius")
        temp = temperature.get("temp")
        temp_min = temperature.get("temp_min")
        temp_max = temperature.get("temp_max")

        results.append("""Location : {} 
        lat : {} 
        lon : {} 
        Time : {} 
        Status: {}
        Detailed: {}
        Temperature: {}°c
        Min temperature: {}°c
        Max temperature: {}°c""" .format(loc_name, loc_lat, loc_lon, time, status, detailed, temp, temp_min, temp_max))

    return "\n".join(results[:10])

if __name__== "__main__":
    print(get_forecasts(-1.2, 36))


