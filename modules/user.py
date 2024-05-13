from flask import render_template, request
from modules import app
from databases.db import Database


# TODO add field search
@app.route("/search", methods=["GET"])
def search_books():
    # check parameters
    if "query" not in request.args:
        error_message = '"query" argument missing'
        return render_template("error.html", data=error_message), 422

    result = []
    for field in ["title", "writer", "publisher"]:
        for row in Database().execute(
            f"SELECT * \
            FROM userbooks \
            WHERE {field} \
            LIKE ?",
            ["%" + request.args["query"] + "%"],
        ):
            result.append(row[1:])

    # toss data to frontend
    data = set(result) if result else None
    return render_template("search.html", data=data)


# TODO checkout books
@app.route("/checkout", methods=["POST"])
def checkout():
    return


# TODO show user profile
@app.route("/profile", methods=["GET"])
def profile():
    return


# TODO apply books
@app.route("/apply", methods=["POST"])
def profile():
    return
