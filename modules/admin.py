from flask import render_template, request
from modules import app
from databases.db import Database
from modules.auth import get_user_info


@app.route("/admin/books/add", methods=["POST"])
def admin_add_books():
    # check role with session
    session = request.cookies.get("session")
    # TODO remove if statement when deploy
    credential = get_user_info(True if session else False)

    # return if role isn't admin
    if credential["role"] != "admin":
        error_messgae = "Not authenticated, You are not admin"
        return render_template("error.html", data=error_messgae), 401

    # check parameters
    data = request.get_json()
    for attr in [
        "available",
        "title",
        "writer",
        "publisher",
        "amount",
        "field",
        "category",
    ]:
        if attr not in data:
            error_messgae = f'"{attr}" not in post data'
            return render_template("error.html", data=error_messgae), 422

    # insert data to db

    Database().execute(
        "INSERT INTO userbooks (available, title, writer, publisher, amount) \
            VALUES (?, ?, ?, ?, ?);",
        (
            data["available"],
            data["title"],
            data["writer"],
            data["publisher"],
            data["amount"],
        ),
    )

    return "", 200


# TODO admin modify books
@app.route("/admin/books/modify", methods=["POST"])
def admin_modify_books():
    return


# TODO admin delete books
@app.route("/admin/books/delete", methods=["POST"])
def admin_delete_books():
    return
