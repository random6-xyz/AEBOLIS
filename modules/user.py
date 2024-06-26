from flask import render_template, request, redirect, url_for
from flask_login import login_required, logout_user, current_user
import time
from datetime import datetime
from modules import app
from databases.db import Database
from modules.auth import get_user_info
from logs.log import save_userbooks_log


# check data has essential parameters
def check_parameters(data, parameters):
    data = request.get_json()
    for attr in parameters:
        if attr not in data:
            error_messgae = f'"{attr}" not in post data'
            return render_template("error.html", data=error_messgae), 422

    return True


# check session
def check_user(session):
    if not session:
        error_messgae = "Not authenticated, You are not user"
        return render_template("error.html", data=error_messgae), 401

    result = get_user_info(session)
    if result == False:
        error_messgae = "Not authenticated, You are not user"
        return render_template("error.html", data=error_messgae), 401

    return result["code"]


# user book search
@app.route("/search", methods=["GET"])
@login_required
def search_books():
    # check parameters
    if "query" not in request.args:
        error_message = '"query" argument missing'
        return render_template("error.html", data=error_message), 422

    # find book data maching with query and [title, writer, publisher]
    query = request.args["query"]
    result = []
    for field in ["title", "writer", "publisher"]:
        for row in Database().execute(
            f"SELECT id FROM userbooks WHERE {field} LIKE ?",
            ["%" + query + "%"],
        ):
            result.append(row[0])

    # find book id matching with query and field
    field_result = Database().execute(
        "SELECT book_id FROM book_field WHERE category=?", [query]
    )

    # query book data and categories with book id
    data_result = []
    for id in set(field_result + result):
        row = Database().execute("SELECT * FROM userbooks WHERE id=?", (str(id),))
        if not row:
            continue
        else:
            row = list(row[0][1:])
        categories = []
        for category in Database().execute(
            "SELECT category FROM book_field WHERE book_id=?", (id,)
        ):
            categories.append(category[0])
        row.append(", ".join(categories))
        data_result.append(row)

    # toss data to frontend
    data = data_result
    return render_template("search.html", data=data)


# user checkout books
@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    data = request.get_json()
    result = check_parameters(data, ["title"])
    if result != True:
        return result

    user_info = get_user_info()
    student_number_result = user_info["id"]
    student_name = user_info["name"]

    # check if books is available
    result = Database().execute(
        "SELECT amount, available FROM userbooks WHERE title=?", (data["title"],)
    )
    if not result:
        error_message = f"No name {data['title']} in DataBase"
        return render_template("error.html", data=error_message), 401
    if result[0][0] <= 0 or result[0][1] == 0:
        error_message = f"You can't borrow {data['title']}"
        return render_template("error.html", data=error_message), 401

    # sub 1 amount
    Database().execute(
        "UPDATE userbooks SET amount=? WHERE title=?", (result[0][0] - 1, data["title"])
    )

    # insert row to checkout_history table
    Database().execute(
        "INSERT INTO checkout_history (student_number, title, return) VALUES (?, ?, 0);",
        (
            int(student_number_result),
            data["title"],
        ),
    )

    # log
    now = time.time()
    dt = datetime.fromtimestamp(now)
    log = {
        "timestamp": str(dt),
        "type": "checkout",
        "student_number": student_number_result,
        "title": data["title"],
        "return": False,
    }
    save_userbooks_log(log)

    return "", 200


# TODO: @imStillDebugging show user profile
@app.route("/profile", methods=["GET"])
@login_required
def profile():
    rows = Database().select_profile_data(current_user.get_id())
    return render_template("user/profile.html", rows=rows)


@app.route("/profile/logs", methods=["GET", "POST"])
@login_required
def profile_log_view():
    if request.method == "POST":
        Database().return_book(current_user.get_id(), request.get_json()["time"])
        return "", 200
    rows = Database().select_book_checkout_list(current_user.get_id())
    return render_template("user/logs.html", rows=rows)


@app.route("/profile/book_apply_list", methods=["GET"])
@login_required
def show_book_apply_list():
    rows = Database().select_book_apply_list(current_user.get_id())
    return render_template("user/book_apply_list.html", rows=rows)


##########################


# user applys books
@app.route("/apply", methods=["POST", "GET"])
@login_required
def apply():
    if request.method == "GET":
        return render_template("apply.html"), 200

    elif request.method == "POST":
        data = request.get_json()
        result = check_parameters(data, ["title", "publisher", "writer", "reason"])
        if result != True:
            return result

        user_info = get_user_info()
        student_number_result = user_info["id"]

        Database().execute(
            "INSERT INTO userapplys (student_number, title, publisher, writer, reason, confirm) VALUES (?, ?, ?, ?, ?, 0)",
            (
                int(student_number_result),
                data["title"],
                data["publisher"],
                data["writer"],
                data["reason"],
            ),
        )

        return "", 200
