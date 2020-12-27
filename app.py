from flasgger import Swagger
from report_pkg import format_delta, create_printer
from flask import Flask, render_template, request, redirect, url_for
from api.routes import api_bp
from utils import make_report_from_db

app = Flask(__name__)
app.register_blueprint(api_bp)
swagger = Swagger(app)

app.jinja_env.globals.update(format_delta=format_delta)

report = make_report_from_db()
printer = create_printer(report)


@app.route("/")
def index_page():
    return redirect(url_for("report_page"))


@app.route("/report/")
def report_page():
    global printer
    if request.args.get("order") == "desc":
        printer = printer[::-1]
    return render_template("report.html", printer=printer)


@app.route("/report/drivers/")
def drivers_page():
    global printer
    if request.args.get("driver_id") in {driver.abbreviation for position, driver in printer}:
        for position, driver in printer:
            if driver.abbreviation == request.args.get("driver_id"):
                return render_template("driver.html", position=position, driver=driver)
    if request.args.get("order") == "desc":
        printer = printer[::-1]
    return render_template("drivers.html", printer=printer)


if __name__ == "__main__":
    app.run(debug=True)
