import paho.mqtt.client as mqtt
import json

class MQTTClient:
    """A wrapper for the paho-mqtt client."""

    def __init__(self, broker, port, client_id="", username=None, password=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv311)
        if username:
            self.client.username_pw_set(username, password)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    def _on_disconnect(self, client, userdata, rc):
        print(f"Disconnected from MQTT Broker with code {rc}")

    def connect(self):
        """Connects to the MQTT broker."""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Error connecting to MQTT Broker: {e}")
            return False

    def disconnect(self):
        """Disconnects from the MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, payload, retain=False):
        """Publishes a message to a topic."""
        # If payload is a dict, convert it to a JSON string
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        
        result = self.client.publish(topic, payload, retain=retain)
        return result
