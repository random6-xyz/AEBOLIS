from flask import render_template
from modules import app
from databases.db import Database


# TODO: @random6 category search
@app.route("/", methods=["GET"])
def index():
    result = Database().execute("SELECT category FROM category")
    return render_template("index.html", data=result), 200
