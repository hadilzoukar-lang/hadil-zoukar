from gpiozero import OutputDevice


class Relay:
    def __init__(self, pin=18, active_high=True):
        self.relay = OutputDevice(
            pin,
            active_high=active_high,
            initial_value=False
        )

    def on(self):
        self.relay.on()

    def off(self):
        self.relay.off()

    def toggle(self):
        self.relay.toggle()

    def is_on(self):
        return self.relay.is_active

    def close(self):
        self.relay.off()
        self.relay.close()
