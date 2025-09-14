"""
Parses the JSON data from the Rainwise IP-100 device.
"""

def parse_sensor_data(data: dict, units: str = 'us') -> dict | None:
    """
    Extracts and flattens the current sensor readings from the raw JSON data.
    Other values are left as comments in the code for easy re-enabling.

    Args:
        data: The raw dictionary parsed from the weather.json file.
        units: The unit system to use ('us' or 'metric'). Defaults to 'us'.

    Returns:
        A dictionary of sensor values or None if the data is invalid.
    """
    if not data or units not in data:
        return None

    measurements = data[units]
    sensors = {}

    # --- Root level sensors ---
    sensors['timestamp'] = data.get('time')
    sensors['battery_volts'] = data.get('batt')
    sensors['signal_dbm'] = data.get('signal')
    sensors['signal_quality'] = data.get('quality')

    # --- Helper to safely get and add nested values ---
    def _add_sensor_family(family_key, name_prefix):
        family_data = measurements.get(family_key, {})
        if not family_data:
            return
        
        # To add more values, uncomment the lines below
        key_map = {
            'ic': '_current', 'tic': '_current', 'ric': '_current', 'bic': '_current', 't1ic': '_current', 't2ic': '_current', 'sic': '_current', 'itic': '_current',
            # 'ia': '_average', 'tia': '_average', 'ria': '_average', 'bia': '_average', 't1ia': '_average', 't2ia': '_average', 'sia': '_average', 'itia': '_average',
            # 'dh': '_today_high', 'tdh': '_today_high', 'rdh': '_today_high', 'bdh': '_today_high', 't1dh': '_today_high', 't2dh': '_today_high', 'sdh': '_today_high', 'itdh': '_today_high',
            # 'ih': '_5min_high', 'tih': '_5min_high', 'rih': '_5min_high', 'bih': '_5min_high', 't1ih': '_5min_high', 't2ih': '_5min_high', 'sih': '_5min_high', 'itih': '_5min_high',
            # 'dl': '_today_low', 'tdl': '_today_low', 'rdl': '_today_low', 'bdl': '_today_low', 't1dl': '_today_low', 't2dl': '_today_low', 'sdl': '_today_low', 'itdl': '_today_low',
            # 'il': '_5min_low', 'til': '_5min_low', 'ril': '_5min_low', 'bil': '_5min_low', 't1il': '_5min_low', 't2il': '_5min_low', 'sil': '_5min_low', 'itil': '_5min_low',
        }
        for key, suffix in key_map.items():
            if key in family_data:
                sensors[name_prefix + suffix] = family_data[key]

    # --- Standard Sensor Families ---
    _add_sensor_family('atmp', 'temp_air')
    _add_sensor_family('rh', 'humidity')
    _add_sensor_family('bp', 'pressure')
    _add_sensor_family('tmp1', 'temp_1')
    _add_sensor_family('tmp2', 'temp_2')
    _add_sensor_family('sm', 'soil_moisture')
    _add_sensor_family('itmp', 'temp_inside')

    # --- Wind (special case) ---
    wind_data = measurements.get('wnd', {})
    if wind_data:
        sensors['wind_speed_current'] = wind_data.get('wic')
        sensors['wind_direction_current'] = wind_data.get('wict')
        # sensors['wind_speed_average'] = wind_data.get('wia')
        # sensors['wind_speed_today_high'] = wind_data.get('wdh')
        # sensors['wind_direction_today_high'] = wind_data.get('wdht')
        # sensors['wind_speed_5min_high'] = wind_data.get('wih')
        # sensors['wind_direction_5min_high'] = wind_data.get('wiht')

    # --- Rainfall (special case) ---
    rain_data = measurements.get('rf', {})
    if rain_data:
        sensors['rain_today'] = rain_data.get('rfd') # This is a total, not a current rate
        # sensors['rain_5min'] = rain_data.get('rfm')

    # --- Solar Radiation (special case) ---
    solar_data = measurements.get('sr', {})
    if solar_data:
        sensors['solar_radiation_current'] = solar_data.get('src')
        # sensors['solar_radiation_today'] = solar_data.get('srd')
        # sensors['solar_radiation_5min'] = solar_data.get('srm')
        
    # --- Solar Radiation 2 (special case) ---
    solar2_data = measurements.get('sr2', {})
    if solar2_data:
        sensors['solar_radiation_2_current'] = solar2_data.get('sr2c')
        # sensors['solar_radiation_2_today'] = solar2_data.get('sr2d')
        # sensors['solar_radiation_2_5min'] = solar2_data.get('sr2m')

    # --- UV (special case) ---
    uv_data = measurements.get('uv', {})
    if uv_data:
        sensors['uv_index_current'] = uv_data.get('uvc')
        # sensors['uv_index_today'] = uv_data.get('uvd')
        # sensors['uv_index_5min'] = uv_data.get('uvm')

    # --- Leaf Wetness (special case) ---
    leaf_data = measurements.get('lw', {})
    if leaf_data:
        sensors['leaf_wetness_current'] = leaf_data.get('lwc')
        # sensors['leaf_wetness_duration_today'] = leaf_data.get('lwd')
        # sensors['leaf_wetness_duration_5min'] = leaf_data.get('lwm')

    # Filter out any sensors that were not found (had a value of None)
    return {k: v for k, v in sensors.items() if v is not None}
