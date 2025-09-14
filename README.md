# Rainwise to MQTT Bridge

This project provides a simple, containerized Python application that polls a local Rainwise IP-100 weather station, parses the sensor data, and publishes it to an MQTT broker. It includes support for Home Assistant's MQTT Discovery, allowing the weather station to be automatically detected and added as a device with multiple sensors in Home Assistant.

## Features

- Polls a Rainwise IP-100's local `weather.json` endpoint.
- Publishes sensor data to an MQTT broker.
- Generates Home Assistant MQTT Discovery configuration for automatic setup.
- All sensors are grouped as a single device in Home Assistant.
- Configurable via environment variables.
- Designed to run as a lightweight Docker container, perfect for servers like Unraid.

## Configuration

The application is configured entirely through environment variables. This is ideal for Docker environments.

| Environment Variable | Default Value | Description |
| :--- | :--- | :--- |
| `RAINWISE_IP` | (None) | **Required.** The IP address of your Rainwise IP-100 device. |
| `MQTT_BROKER` | (None) | **Required.** The hostname or IP address of your MQTT broker. |
| `MQTT_PORT` | `1883` | The port of your MQTT broker. |
| `MQTT_USERNAME` | (None) | The username for your MQTT broker (if any). |
| `MQTT_PASSWORD` | (None) | The password for your MQTT broker (if any). |
| `POLL_INTERVAL` | `60` | The number of seconds to wait between polling the weather station. |
| `WIND_DIRECTION_OFFSET` | `0` | A positive or negative integer to offset the wind direction in degrees for calibration. |

**Note:** While the script has some of these values set as defaults for testing, it is best practice to provide them explicitly as environment variables when you run the container.

## Docker Usage

### Building the Image

To build the Docker image, navigate to the project's root directory (where the `Dockerfile` is located) and run:

```bash
docker build -t rainwise-to-mqtt .
```

### Running the Container

To run the container, you must provide the necessary environment variables. Here is an example `docker run` command. You can adapt this for Unraid's "Add Container" screen.

```bash
docker run -d \
  --name rainwise-mqtt \
  -e RAINWISE_IP="192.168.86.207" \
  -e MQTT_BROKER="192.168.86.33" \
  -e MQTT_PORT="1883" \
  -e MQTT_USERNAME="localDevices" \
  -e MQTT_PASSWORD="d0gf00d" \
  -e POLL_INTERVAL="60" \
  -e WIND_DIRECTION_OFFSET="0" \
  --restart unless-stopped \
  rainwise-to-mqtt
```

On Unraid, you would use the "Add Container" page, set the repository to `rainwise-to-mqtt`, and then add each of the environment variables from the example above using the "Add another Path, Port, Variable, Label or Device" button.

```
