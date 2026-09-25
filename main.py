import time
import threading

from sensors.dht22 import DHT22Sensor
from sensors.pir import PIRSensor

from actuators.relay import Relay
from actuators.buzzer import AlarmBuzzer

from automation.rules import AutomationRules
from database.database import Database

from web.app import create_app


# ==============================
# Configuration
# ==============================

SENSOR_PERIOD = 5


# ==============================
# Initialisation
# ==============================

print("Initialisation du système...")

database = Database()

dht22 = DHT22Sensor()
pir = PIRSensor()

relay = Relay(pin=18)
buzzer = AlarmBuzzer(pin=23)

rules = AutomationRules(
    relay=relay,
    buzzer=buzzer,
    database=database
)


# ==============================
# Application Web
# ==============================

app = create_app(
    relay=relay,
    rules=rules,
    database=database
)


# ==============================
# Tâche principale
# ==============================

def sensor_loop():

    last_motion = False

    while True:

        # ----------------------
        # Lecture DHT22
        # ----------------------

        temperature, humidity = dht22.read()

        if temperature is not None:

            print(
                f"Température : {temperature:.1f} °C"
            )

            print(
                f"Humidité    : {humidity:.1f} %"
            )

            database.add_measurement(
                temperature,
                humidity
            )

            app.temperature = round(
                temperature,
                1
            )

            app.humidity = round(
                humidity,
                1
            )

        # ----------------------
        # Lecture PIR
        # ----------------------

        motion = pir.is_motion_detected()

        app.motion = motion

        # Détection d'un nouveau mouvement
        if motion and not last_motion:

            print("Mouvement détecté !")

            rules.process_motion(True)

        last_motion = motion

        time.sleep(SENSOR_PERIOD)


# ==============================
# Démarrage
# ==============================

if __name__ == "__main__":

    try:

        print("Démarrage du système domotique...")

        thread = threading.Thread(
            target=sensor_loop,
            daemon=True
        )

        thread.start()

        app.run(
            host="0.0.0.0",
            port=5000,
            debug=False
        )

    except KeyboardInterrupt:

        print("\nArrêt du système...")

    finally:

        relay.off()

        dht22.close()
        relay.close()
        buzzer.close()
