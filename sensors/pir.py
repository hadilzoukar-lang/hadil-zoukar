from gpiozero import MotionSensor


class PIRSensor:
    def __init__(self, pin=17):
        self.sensor = MotionSensor(pin)

    def is_motion_detected(self):
        return self.sensor.motion_detected
