from flasgger import Swagger
from report_pkg import format_delta
from flask import Flask, render_template, request, redirect, url_for
from api.resources import api_bp, printer, drivers_id_set

app = Flask(__name__)
app.register_blueprint(api_bp)
swagger = Swagger(app)

app.jinja_env.globals.update(format_delta=format_delta)


@app.route("/")
def index_page():
    return redirect(url_for("report_page"))


@app.route("/report/")
def report_page():
    data = printer[:]
    if request.args.get("order") == "desc":
        data = data[::-1]
    return render_template("report.html", printer=data)


@app.route("/report/drivers/")
def drivers_page():
    data = printer[:]
    if request.args.get("driver_id") in drivers_id_set:
        for position, driver in data:
            if driver.abbreviation == request.args.get("driver_id"):
                return render_template("driver.html", position=position, driver=driver)
    if request.args.get("order") == "desc":
        data = data[::-1]
    return render_template("drivers.html", printer=data)


if __name__ == "__main__":
    app.run(debug=True)
