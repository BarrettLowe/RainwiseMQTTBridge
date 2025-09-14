import json

# A mapping of sensor keys to their Home Assistant metadata.
# This defines the name, unit, device_class, and icon for each sensor.
SENSOR_METADATA = {
    "battery_volts": {"name": "Battery", "unit": "V", "class": "voltage"},
    "signal_dbm": {"name": "Signal Strength", "unit": "dBm", "class": "signal_strength"},
    "temp_air_current": {"name": "Air Temperature", "unit": "°F", "class": "temperature"},
    "humidity_current": {"name": "Humidity", "unit": "%", "class": "humidity"},
    "pressure_current": {"name": "Barometric Pressure", "unit": "inHg", "class": "pressure"},
    "wind_speed_current": {"name": "Wind Speed", "unit": "mph", "icon": "mdi:weather-windy"},
    "wind_direction_degrees": {"name": "Wind Direction Degrees", "unit": "°", "icon": "mdi:compass-outline"},
    "wind_direction_cardinal": {"name": "Wind Direction", "unit": "", "icon": "mdi:compass-rose"},
    "rain_today": {"name": "Rain Today", "unit": "in", "icon": "mdi:weather-rainy"},
    "solar_radiation_current": {"name": "Solar Radiation", "unit": "W/m²", "icon": "mdi:weather-sunny"},
    "leaf_wetness_current": {"name": "Leaf Wetness", "unit": "", "icon": "mdi:leaf"},
    "temp_1_current": {"name": "Probe Temperature 1", "unit": "°F", "class": "temperature"},
    "soil_moisture_current": {"name": "Soil Moisture", "unit": "cb (kPa)", "icon": "mdi:water-percent"},
    "temp_inside_current": {"name": "Inside Temperature", "unit": "°F", "class": "temperature"},
}

def generate_discovery_configs(parsed_data: dict, state_topic: str, device_info: dict) -> list:
    """
    Generates a list of Home Assistant MQTT discovery configurations.

    Args:
        parsed_data: The dictionary of parsed sensor data.
        state_topic: The MQTT topic where sensor state is published.
        device_info: The common device information dictionary.

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
