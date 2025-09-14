import os
import json
import time
from fetch import get_weather_data
from parse import parse_sensor_data
from mqtt import MQTTClient
from ha_discovery import generate_discovery_configs

# --- Configuration ---
RAINWISE_IP = os.getenv("RAINWISE_IP", "192.168.86.207")
MQTT_BROKER = os.getenv("MQTT_BROKER", "192.168.86.33")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "localDevices")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "d0gf00d")
MQTT_STATE_TOPIC = "rainwise/station/state"
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 60))  # seconds

# --- Home Assistant Device Info ---
# This information will be used for all sensors to group them into a single device.
DEVICE_INFO = {
    "identifiers": ["rainwise_ip100_station"],
    "name": "Rainwise IP-100 Weather Station",
    "model": "IP-100",
    "manufacturer": "Rainwise",
}


def main():
    """Main application loop."""
    print("--- Starting Rainwise to MQTT Bridge ---")

    # --- Connect to MQTT ---
    mqtt_client = MQTTClient(MQTT_BROKER, MQTT_PORT, username=MQTT_USERNAME, password=MQTT_PASSWORD)
    if not mqtt_client.connect():
        print("Failed to connect to MQTT. Exiting.")
        return
    
    time.sleep(1)  # Give client time to establish connection

    # --- Main Loop ---
    try:
        discovery_published = False
        while True:
            # --- 1. Fetch and Parse Data ---
            raw_data = get_weather_data(RAINWISE_IP)
            if not raw_data:
                print(f"[ERROR] Could not retrieve data. Retrying in {POLL_INTERVAL} seconds...")
                time.sleep(POLL_INTERVAL)
                continue

            sensors = parse_sensor_data(raw_data)
            if not sensors:
                print(f"[ERROR] Failed to parse sensor data. Retrying in {POLL_INTERVAL} seconds...")
                time.sleep(POLL_INTERVAL)
                continue
            
            # --- 2. Publish HA Discovery (only on first successful run) ---
            if not discovery_published:
                print("Publishing Home Assistant discovery messages...")
                discovery_configs = generate_discovery_configs(sensors, MQTT_STATE_TOPIC, DEVICE_INFO)
                for topic, payload in discovery_configs:
                    mqtt_client.publish(topic, payload, retain=True)
                discovery_published = True
                print(f"Published {len(discovery_configs)} discovery messages.")

            # --- 3. Publish Data ---
            mqtt_client.publish(MQTT_STATE_TOPIC, sensors)

            # --- 4. Wait for next poll ---
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nShutdown requested.")
    finally:
        # --- 5. Disconnect ---
        print("Disconnecting from MQTT broker.")
        mqtt_client.disconnect()

    print("--- Application stopped ---")


if __name__ == "__main__":
    main()
