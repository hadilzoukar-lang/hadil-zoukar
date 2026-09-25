class AutomationRules:

    def __init__(self, relay, buzzer, database):
        self.relay = relay
        self.buzzer = buzzer
        self.database = database

        self.automatic_mode = True
        self.alarm_enabled = False

    def process_motion(self, motion_detected):

        if not motion_detected:
            return

        if self.automatic_mode:
            self.relay.on()
            self.database.add_event(
                "Mouvement détecté - lumière ON"
            )

        if self.alarm_enabled:
            self.buzzer.beep()
            self.database.add_event(
                "ALARME - mouvement détecté"
            )

    def set_automatic_mode(self, enabled):
        self.automatic_mode = enabled

    def set_alarm(self, enabled):
        self.alarm_enabled = enabled
