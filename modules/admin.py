from flask import render_template, request
from modules import app
from databases.db import Database
from modules.auth import get_user_info


# check data has essential parameters
def check_parameters(data, parameters):
    data = request.get_json()
    for attr in parameters:
        if attr not in data:
            error_messgae = f'"{attr}" not in post data'
            return render_template("error.html", data=error_messgae), 422

    return True


# check session is admin's
def check_admin(session):
    # check session exists
    if not session:
        error_messgae = "Not authenticated, You are not admin"
        return render_template("error.html", data=error_messgae), 401
    # TODO remove if statement when deploy
    credential = get_user_info(True if session else False)
    # return if role isn't admin
    if credential["role"] != "admin":
        error_messgae = "Not authenticated, You are not admin"
        return render_template("error.html", data=error_messgae), 401

    return True


# check parameters and role
def check_parameters_admin(data, parameters, session):
    # check role with session
    result = check_parameters(data, parameters)
    if result != True:
        return result

    # check parameters
    result = check_admin(session)
    if result != True:
        return result

    return True


@app.route("/admin/books/add", methods=["POST"])
def admin_add_books():
    data = request.get_json()
    result = check_parameters_admin(
        data,
        ["available", "title", "writer", "publisher", "amount"],
        request.cookies.get("session"),
    )
    if result != True:
        return result

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


@app.route("/admin/books/show", methods=["GET"])
def admin_show_books():
    result = check_admin(True if request.cookies.get("session") else False)
    if result != True:
        return result

    db_result = Database().execute(
        "SELECT available, title, writer, publisher, amount FROM userbooks"
    )
    if not db_result:
        error_message = "There are no books"
        return render_template("error.html", data=error_message), 401

    return render_template("admin/books.html", data=db_result)


# TODO admin modify books
@app.route("/admin/books/modify", methods=["POST"])
def admin_modify_books():
    return


# TODO admin delete books
@app.route("/admin/books/delete", methods=["POST"])
def admin_delete_books():

    return


# TODO admin show logs
@app.route("/admin/logs", methods=["GET"])
def admin_logs():
    return


# TODO admin show users
@app.route("/admin/users", methods=["GET"])
def admin_show_users():
    return


# TODO admin modify users
@app.route("/admin/users/modify", methods=["POST"])
def admin_modify_users():
    return
