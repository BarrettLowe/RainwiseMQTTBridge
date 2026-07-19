import json

# A mapping of sensor keys to their Home Assistant metadata.
# This defines the name, unit, device_class, and icon for each sensor.
SENSOR_METADATA = {
    "battery_volts": {"name": "Battery", "unit": "V", "class": "voltage"},
    "signal_dbm": {"name": "Signal Strength", "unit": "dBm", "class": "signal_strength"},
    "signal_quality": {"name": "Signal Quality", "icon": "mdi:signal-cellular-outline"},

    "temp_air_current": {"name": "Air Temperature", "unit": "°F", "class": "temperature"},
    "temp_air_average": {"name": "Air Temperature Average", "unit": "°F", "class": "temperature"},
    "temp_air_today_high": {"name": "Air Temperature Today High", "unit": "°F", "class": "temperature"},
    "temp_air_5min_high": {"name": "Air Temperature 5min High", "unit": "°F", "class": "temperature"},
    "temp_air_today_low": {"name": "Air Temperature Today Low", "unit": "°F", "class": "temperature"},
    "temp_air_5min_low": {"name": "Air Temperature 5min Low", "unit": "°F", "class": "temperature"},

    "humidity_current": {"name": "Humidity", "unit": "%", "class": "humidity"},
    "humidity_average": {"name": "Humidity Average", "unit": "%", "class": "humidity"},
    "humidity_today_high": {"name": "Humidity Today High", "unit": "%", "class": "humidity"},
    "humidity_5min_high": {"name": "Humidity 5min High", "unit": "%", "class": "humidity"},
    "humidity_today_low": {"name": "Humidity Today Low", "unit": "%", "class": "humidity"},
    "humidity_5min_low": {"name": "Humidity 5min Low", "unit": "%", "class": "humidity"},

    "pressure_current": {"name": "Barometric Pressure", "unit": "inHg", "class": "pressure"},
    "pressure_average": {"name": "Barometric Pressure Average", "unit": "inHg", "class": "pressure"},
    "pressure_today_high": {"name": "Barometric Pressure Today High", "unit": "inHg", "class": "pressure"},
    "pressure_5min_high": {"name": "Barometric Pressure 5min High", "unit": "inHg", "class": "pressure"},
    "pressure_today_low": {"name": "Barometric Pressure Today Low", "unit": "inHg", "class": "pressure"},
    "pressure_5min_low": {"name": "Barometric Pressure 5min Low", "unit": "inHg", "class": "pressure"},

    "wind_speed_current": {"name": "Wind Speed", "unit": "mph", "icon": "mdi:weather-windy"},
    "wind_speed_average": {"name": "Wind Speed Average", "unit": "mph", "icon": "mdi:weather-windy"},
    "wind_direction_degrees": {"name": "Wind Direction Degrees", "unit": "°", "icon": "mdi:compass-outline"},
    "wind_direction_cardinal": {"name": "Wind Direction", "icon": "mdi:compass-rose"},
    "wind_gust_speed_today": {"name": "Wind Gust Speed Today", "unit": "mph", "icon": "mdi:weather-windy-variant"},
    "wind_gust_direction_today_degrees": {"name": "Wind Gust Direction Today Degrees", "unit": "°", "icon": "mdi:compass-outline"},
    "wind_gust_direction_today_cardinal": {"name": "Wind Gust Direction Today", "icon": "mdi:compass-rose"},
    "wind_gust_speed_5min": {"name": "Wind Gust Speed 5min", "unit": "mph", "icon": "mdi:weather-windy-variant"},
    "wind_gust_direction_5min_degrees": {"name": "Wind Gust Direction 5min Degrees", "unit": "°", "icon": "mdi:compass-outline"},
    "wind_gust_direction_5min_cardinal": {"name": "Wind Gust Direction 5min", "icon": "mdi:compass-rose"},

    "rain_today": {"name": "Rain Today", "unit": "in", "icon": "mdi:weather-rainy"},
    "rain_5min": {"name": "Rain 5min", "unit": "in", "icon": "mdi:weather-rainy"},

    # No documented unit for these — device groups them as current/day/5min (accumulator-style),
    # not current/avg/hi/lo, so day/5min are very likely a different unit than the instantaneous
    # W/m² reading (e.g. accumulated energy). Left unitless rather than guessing wrong.
    "solar_radiation_current": {"name": "Solar Radiation", "unit": "W/m²", "icon": "mdi:weather-sunny"},
    "solar_radiation_today": {"name": "Solar Radiation Today Total", "icon": "mdi:weather-sunny"},
    "solar_radiation_5min": {"name": "Solar Radiation 5min Total", "icon": "mdi:weather-sunny"},
    "solar_radiation_2_current": {"name": "Solar Radiation 2", "unit": "W/m²", "icon": "mdi:weather-sunny"},
    "solar_radiation_2_today": {"name": "Solar Radiation 2 Today Total", "icon": "mdi:weather-sunny"},
    "solar_radiation_2_5min": {"name": "Solar Radiation 2 5min Total", "icon": "mdi:weather-sunny"},

    "uv_index_current": {"name": "UV Index", "icon": "mdi:sun-wireless"},
    "uv_index_today": {"name": "UV Index Today", "icon": "mdi:sun-wireless"},
    "uv_index_5min": {"name": "UV Index 5min", "icon": "mdi:sun-wireless"},

    "leaf_wetness_current": {"name": "Leaf Wetness", "icon": "mdi:leaf"},
    "leaf_wetness_duration_today": {"name": "Leaf Wetness Duration Today", "unit": "min", "icon": "mdi:leaf"},
    "leaf_wetness_duration_5min": {"name": "Leaf Wetness Duration 5min", "unit": "min", "icon": "mdi:leaf"},

    "temp_1_current": {"name": "Probe Temperature 1", "unit": "°F", "class": "temperature"},
    "temp_1_average": {"name": "Probe Temperature 1 Average", "unit": "°F", "class": "temperature"},
    "temp_1_today_high": {"name": "Probe Temperature 1 Today High", "unit": "°F", "class": "temperature"},
    "temp_1_5min_high": {"name": "Probe Temperature 1 5min High", "unit": "°F", "class": "temperature"},
    "temp_1_today_low": {"name": "Probe Temperature 1 Today Low", "unit": "°F", "class": "temperature"},
    "temp_1_5min_low": {"name": "Probe Temperature 1 5min Low", "unit": "°F", "class": "temperature"},

    "temp_2_current": {"name": "Probe Temperature 2", "unit": "°F", "class": "temperature"},
    "temp_2_average": {"name": "Probe Temperature 2 Average", "unit": "°F", "class": "temperature"},
    "temp_2_today_high": {"name": "Probe Temperature 2 Today High", "unit": "°F", "class": "temperature"},
    "temp_2_5min_high": {"name": "Probe Temperature 2 5min High", "unit": "°F", "class": "temperature"},
    "temp_2_today_low": {"name": "Probe Temperature 2 Today Low", "unit": "°F", "class": "temperature"},
    "temp_2_5min_low": {"name": "Probe Temperature 2 5min Low", "unit": "°F", "class": "temperature"},

    "soil_moisture_current": {"name": "Soil Moisture", "unit": "cb (kPa)", "icon": "mdi:water-percent"},
    "soil_moisture_average": {"name": "Soil Moisture Average", "unit": "cb (kPa)", "icon": "mdi:water-percent"},
    "soil_moisture_today_high": {"name": "Soil Moisture Today High", "unit": "cb (kPa)", "icon": "mdi:water-percent"},
    "soil_moisture_5min_high": {"name": "Soil Moisture 5min High", "unit": "cb (kPa)", "icon": "mdi:water-percent"},
    "soil_moisture_today_low": {"name": "Soil Moisture Today Low", "unit": "cb (kPa)", "icon": "mdi:water-percent"},
    "soil_moisture_5min_low": {"name": "Soil Moisture 5min Low", "unit": "cb (kPa)", "icon": "mdi:water-percent"},

    "temp_inside_current": {"name": "Inside Temperature", "unit": "°F", "class": "temperature"},
    "temp_inside_average": {"name": "Inside Temperature Average", "unit": "°F", "class": "temperature"},
    "temp_inside_today_high": {"name": "Inside Temperature Today High", "unit": "°F", "class": "temperature"},
    "temp_inside_5min_high": {"name": "Inside Temperature 5min High", "unit": "°F", "class": "temperature"},
    "temp_inside_today_low": {"name": "Inside Temperature Today Low", "unit": "°F", "class": "temperature"},
    "temp_inside_5min_low": {"name": "Inside Temperature 5min Low", "unit": "°F", "class": "temperature"},
}

def generate_discovery_configs(parsed_data: dict, state_topic: str, device_info: dict, availability_topic: str) -> list:
    """
    Generates a list of Home Assistant MQTT discovery configurations.

    Args:
        parsed_data: The dictionary of parsed sensor data.
        state_topic: The MQTT topic where sensor state is published.
        device_info: The common device information dictionary.
        availability_topic: The MQTT topic for device availability.

    Returns:
        A list of tuples, where each tuple is (discovery_topic, config_payload).
    """
    configs = []
    for key, value in parsed_data.items():
        if key not in SENSOR_METADATA:
            continue

        meta = SENSOR_METADATA[key]
        sensor_id = f"rainwise_{key}"
        discovery_topic = f"homeassistant/sensor/{sensor_id}/config"

        payload = {
            "name": meta["name"],
            "unique_id": sensor_id,
            "state_topic": state_topic,
            "value_template": f"{{{{ value_json.{key} }}}}",
            "availability_topic": availability_topic,
            "payload_available": "online",
            "payload_not_available": "offline",
            "device": device_info,
        }

        if meta.get("unit"):
            payload["unit_of_measurement"] = meta["unit"]
        if meta.get("class"):
            payload["device_class"] = meta["class"]
        if meta.get("icon"):
            payload["icon"] = meta["icon"]

        configs.append((discovery_topic, json.dumps(payload)))
    
    return configs
