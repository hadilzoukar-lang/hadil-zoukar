import board
import adafruit_dht


class DHT22Sensor:
    def __init__(self, pin=board.D4):
        self.sensor = adafruit_dht.DHT22(pin, use_pulseio=False)

    def read(self):
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity

            if temperature is None or humidity is None:
                return None, None

            return temperature, humidity

        except RuntimeError:
            # Le DHT22 peut occasionnellement rater une lecture.
            return None, None

    def close(self):
        self.sensor.exit()
