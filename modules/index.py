from flask import render_template
from modules import app
from databases.db import Database


@app.route("/", methods=["GET"])
def index():
    result = Database().execute("SELECT category FROM category")
    return render_template("index.html", data=result), 200


@app.route("/admin", methods=["GET"])
def admin_index():
    return render_template("admin/index.html"), 200
