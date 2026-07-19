# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small containerized Python daemon that polls a Rainwise IP-100 weather station's local `weather.json` endpoint, parses the sensor readings, and publishes them to an MQTT broker with Home Assistant MQTT Discovery support. No test suite, no linter config — this is a ~5-file script-sized project, not a framework.

## Running it

There's no test suite or lint tooling configured. Development is run-it-and-look-at-the-output.

```bash
pip install -r requirements.txt
python src/main.py
```

Config is entirely via environment variables (see README.md for the full table: `RAINWISE_IP`, `MQTT_BROKER`, `MQTT_PORT`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `POLL_INTERVAL`, `WIND_DIRECTION_OFFSET`). `src/main.py` has hardcoded fallback defaults for local testing — the README notes these should always be overridden explicitly in real deployments.

Docker build/run:

```bash
docker build -t rainwise-to-mqtt .
docker run -d --name rainwise-mqtt -e RAINWISE_IP=... -e MQTT_BROKER=... rainwise-to-mqtt
```

CI (`.github/workflows/docker-publish.yml`) auto-builds and pushes a multi-arch (amd64/arm64) image to Docker Hub as `barrettlowe/rainwise-to-mqtt:dev` on every push to `main`. There's no test gate in that workflow — pushing to `main` publishes directly.

## Architecture

Linear pipeline, one module per stage, wired together in `src/main.py`'s poll loop:

```
fetch.py  →  parse.py  →  ha_discovery.py  →  mqtt.py
(HTTP GET)   (flatten)     (HA config gen)     (publish)
```

- **`fetch.py`** — `get_weather_data(ip)`: single HTTP GET against `http://{ip}/weather.json`. Returns `None` on any network/JSON error (never raises) — callers must check for `None`.
- **`parse.py`** — `parse_sensor_data(data, units, wind_offset)`: the station's raw JSON is deeply nested and keyed with terse device-specific codes (e.g. `wnd.wic`, `atmp.ic`). This flattens it into flat, human-named keys (`wind_speed_current`, `temp_air_current`, ...). Most of the raw fields the device exposes (averages, daily highs/lows, etc.) are deliberately *not* extracted — see the commented-out `key_map` entries and per-family blocks; uncomment there to add a field rather than adding new parsing logic elsewhere. Also computes `has_sensor_data` (device reports all-zero/sentinel values when no physical sensors are attached, used to drive HA availability) and applies `wind_offset` for compass calibration, wrapping mod 360.
- **`ha_discovery.py`** — `generate_discovery_configs(...)`: builds Home Assistant MQTT Discovery payloads from a single `SENSOR_METADATA` dict (name/unit/device_class/icon per sensor key). **Adding a new sensor requires two places to agree**: the key must exist both here in `SENSOR_METADATA` and as an output key of `parse_sensor_data` — a parsed key with no matching metadata entry is silently skipped and never gets a discovery config.
- **`mqtt.py`** — thin wrapper (`MQTTClient`) around `paho-mqtt`; auto-serializes dict payloads to JSON on publish.
- **`main.py`** — owns the poll loop: fetch → parse → (publish HA discovery once, on first successful poll only) → publish state → sleep `POLL_INTERVAL` → repeat. Also manages the availability topic (`online`/`offline`, retained) based on `has_sensor_data`.

### Adding a new sensor

1. Add extraction logic in `parse.py` (uncomment the relevant `key_map` entry, or extend a special-case block like wind/rain/solar if the field needs custom handling).
2. Add a matching entry in `SENSOR_METADATA` in `ha_discovery.py` with the same key.

Both steps are required — missing either one means the value either doesn't get parsed, or gets published to MQTT but never shows up in Home Assistant.
