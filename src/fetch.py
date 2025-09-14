import requests

def get_weather_data(ip_address: str) -> dict | None:
    """
    Fetches weather data from the Rainwise IP-100's weather.json file.

    Args:
        ip_address: The IP address of the Rainwise IP-100 device.

    Returns:
        A dictionary containing the weather data, or None if an error occurs.
    """
    url = f"http://{ip_address}/weather.json"
    print(f"Fetching data from {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None
