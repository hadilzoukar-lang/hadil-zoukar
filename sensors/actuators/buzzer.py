from gpiozero import Buzzer


class AlarmBuzzer:
    def __init__(self, pin=23):
        self.buzzer = Buzzer(pin)

    def on(self):
        self.buzzer.on()

    def off(self):
        self.buzzer.off()

    def beep(self, duration=0.2):
        self.buzzer.beep(
            on_time=duration,
            off_time=duration,
            n=1,
            background=False
        )

    def close(self):
        self.buzzer.off()
        self.buzzer.close()
