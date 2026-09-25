from flask import Flask, render_template, redirect, url_for


def create_app(relay, rules, database):

    app = Flask(__name__)

    @app.route("/")
    def index():

        measurements = database.get_measurements(10)
        events = database.get_events(10)

        return render_template(
            "index.html",
            temperature=getattr(app, "temperature", None),
            humidity=getattr(app, "humidity", None),
            motion=getattr(app, "motion", False),
            light=relay.is_on(),
            automatic=rules.automatic_mode,
            alarm=rules.alarm_enabled,
            measurements=measurements,
            events=events
        )

    @app.route("/light/on")
    def light_on():

        relay.on()
        database.add_event("Commande manuelle : lumière ON")

        return redirect(url_for("index"))

    @app.route("/light/off")
    def light_off():

        relay.off()
        database.add_event("Commande manuelle : lumière OFF")

        return redirect(url_for("index"))

    @app.route("/automatic/on")
    def automatic_on():

        rules.set_automatic_mode(True)
        database.add_event("Mode automatique activé")

        return redirect(url_for("index"))

    @app.route("/automatic/off")
    def automatic_off():

        rules.set_automatic_mode(False)
        database.add_event("Mode automatique désactivé")

        return redirect(url_for("index"))

    @app.route("/alarm/on")
    def alarm_on():

        rules.set_alarm(True)
        database.add_event("Alarme activée")

        return redirect(url_for("index"))

    @app.route("/alarm/off")
    def alarm_off():

        rules.set_alarm(False)
        database.add_event("Alarme désactivée")

        return redirect(url_for("index"))

    return app
