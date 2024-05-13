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


# TODO @random6 add field search
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


# TODO @random6 add row to checkout history table
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

    return "", 200


# TODO @imStillDebugging show user profile
@app.route("/profile", methods=["GET"])
def profile():
    return


# user applys books
@app.route("/apply", methods=["POST"])
def apply():
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
