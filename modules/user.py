from flask import render_template, request
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


# TODO: @random6 category search
# user book search
@app.route("/search", methods=["GET"])
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
        row = list(
            Database().execute("SELECT * FROM userbooks WHERE id=?", (id,))[0][1:]
        )
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
def checkout():
    data = request.get_json()
    result = check_parameters(data, ["title"])
    if result != True:
        return result

    student_number_result = check_user(request.cookies.get("session"))
    if type(student_number_result) != str:
        return student_number_result

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
def profile():
    return


# user applys books
@app.route("/apply", methods=["POST", "GET"])
def apply():
    result = check_user(request.cookies.get("session"))
    if not result:
        return result

    if request.method == "GET":
        return render_template("apply.html"), 200

    elif request.method == "POST":
        data = request.get_json()
        result = check_parameters(data, ["title", "publisher", "writer", "reason"])
        if result != True:
            return result

        student_number_result = check_user(request.cookies.get("session"))
        if type(student_number_result) != str:
            return student_number_result

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
