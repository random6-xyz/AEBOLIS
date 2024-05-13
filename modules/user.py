from flask import render_template
from modules import app
from databases.db import Database


@app.route("/search")
def search_books():
    Database().execute(";")
    return render_template("search.html")
