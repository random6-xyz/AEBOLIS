from flask import render_template, request
from modules import app
from databases.db import Database


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
            result.append(row)

    # toss data to frontend
    data = result if result else None
    return render_template("search.html", data=data[1:])
