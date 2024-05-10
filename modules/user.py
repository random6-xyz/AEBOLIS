from flask import render_template, request
from modules import app
from databases.db import Database


@app.route("/search", methods=["GET"])
def search_books():
    if "query" not in request.args:
        error_message = '"query" argument missing'
        return render_template("error.html", data=error_message), 422

    Database().execute(";")
    return render_template("search.html")
