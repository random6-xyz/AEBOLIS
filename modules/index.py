from flask import render_template
from modules import app


# TODO: @random6 category search
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html"), 200
