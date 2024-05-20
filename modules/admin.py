from flask import render_template, request
from pandas import read_excel
from werkzeug.utils import secure_filename
from modules import app
from databases.db import Database
from modules.auth import get_user_info
from logs.log import *


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
    # FIXME: @random6 remove if statement when deploy
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


@app.route("/admin/books", methods=["GET"])
def admin_books():
    result = check_admin(request.cookies.get("session"))
    if result != True:
        return result

    book_data = []

    for book_info in Database().execute("SELECT * FROM userbooks"):
        id, book_info_data = book_info[0], book_info[1:]
        tmp_book_info = []
        for book_field in Database().execute(
            "SELECT category FROM book_field WHERE book_id=?", (id,)
        ):
            tmp_book_info.append(*book_field)

        book_info_data = list(book_info_data)
        book_info_data.append(", ".join(tmp_book_info))
        book_data.append(book_info_data)

    return render_template("admin/books.html", data=book_data), 200


# add books
@app.route("/admin/books/add", methods=["POST", "GET"])
def admin_add_books():
    if request.method == "GET":
        result = check_admin(request.cookies.get("session"))
        if result != True:
            return result
        return render_template("admin/add_book.html"), 200

    elif request.method == "POST":
        data = request.get_json()
        result = check_parameters_admin(
            data,
            ["available", "title", "writer", "publisher", "amount", "field"],
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

        book_id = Database().execute(
            "SELECT id FROM userbooks WHERE title=?", (data["title"],)
        )

        for field in data["field"].split(","):
            Database().execute(
                "INSERT INTO book_field (book_id, category) VALUES (?, ?)",
                (
                    book_id[0][0],
                    field.strip(),
                ),
            )

        return "", 200


# modifying books for admin
@app.route("/admin/books/modify", methods=["POST", "GET"])
def admin_modify_books():
    result = check_admin(request.cookies.get("session"))
    if result != True:
        return result

    # return modify pages
    if request.method == "GET":

        data = request.args
        # for (key, value) in request.args:
        # data[key] = value
        return render_template("admin/modify.html", data=data), 200

    # book modifying process
    if request.method == "POST":
        data = request.get_json()
        result = check_parameters(
            data,
            [
                "old_title",
                "available",
                "title",
                "writer",
                "publisher",
                "amount",
                "category",
            ],
        )
        if result != True:
            return result

        # Update userbooks table
        Database().execute(
            "UPDATE userbooks SET available=?, title=?, writer=?, publisher=?, amount=? WHERE title=?",
            (
                data["available"].strip(),
                data["title"].strip(),
                data["writer"].strip(),
                data["publisher"].strip(),
                data["amount"].strip(),
                data["old_title"].strip(),
            ),
        )

        # Update book_field table
        id = Database().execute(
            "SELECT id FROM userbooks WHERE title=?", (data["title"].strip(),)
        )[0][0]
        print(id)
        Database().execute("DELETE FROM book_field WHERE book_id=?", (id,))
        for category in data["category"].split(","):
            Database().execute(
                "INSERT INTO book_field (book_id, category) VALUES (?, ?)",
                (
                    id,
                    category,
                ),
            )

        return "", 200


# admin delete book
@app.route("/admin/books/delete", methods=["POST"])
def admin_delete_books():
    data = request.get_json()
    result = check_parameters_admin(
        data,
        ["title"],
        request.cookies.get("session"),
    )
    if result != True:
        return result

    db = Database()

    id = db.execute("SELECT id FROM userbooks WHERE title=?", (data["title"],))[0][0]
    db.execute("DELETE FROM userbooks WHERE title=?", (data["title"],))
    db.execute("DELETE FROM book_field WHERE book_id=?", (id,))

    return "", 200


# admin modify logs
@app.route("/admin/logs", methods=["GET", "POST"])
def admin_logs():
    result = check_admin(request.cookies.get("session"))
    if result != True:
        return result

    if request.method == "GET":
        # get logs and return
        logs = load_userbooks_log()
        print(logs)
        return render_template("admin/logs.html", data=logs), 200

    elif request.method == "POST":
        data = request.get_json()
        result = check_parameters(
            data, ["timestamp", "type", "student_number", "title", "return"]
        )
        if result != True:
            return result

        logs = load_userbooks_log()
        for index, log in enumerate(logs):
            if log["timestamp"] == data["timestamp"]:
                logs[index]["timestamp"] = data["timestamp"]
                logs[index]["type"] = data["type"]
                logs[index]["student_number"] = data["student_number"]
                logs[index]["title"] = data["title"]
                logs[index]["return"] = data["return"]

        reset_uesrbooks_log(logs)
        return "", 200


# admin show applys
@app.route("/admin/apply", methods=["GET", "POST"])
def admin_apply():
    result = check_admin(request.cookies.get("session"))
    if result != True:
        return result

    # show apply to admin
    if request.method == "GET":
        data = Database().execute(
            "SELECT student_number, title, publisher, writer, reason, confirm FROM userapplys"
        )
        return render_template("admin/apply.html", data=data), 200

    # modify apply
    elif request.method == "POST":
        data = request.get_json()
        result = check_parameters(data, ["title", "method", "student_number"])
        if result != True:
            return result

        if data["method"] == "delete":
            Database().execute(
                "DELETE FROM userapplys WHERE title=? and student_number=?",
                (
                    data["title"],
                    data["student_number"],
                ),
            )
            return "", 200

        elif data["method"] == "confirm":
            Database().execute(
                "UPDATE userapplys SET confirm=1 WHERE title=? and student_number=?",
                (
                    data["title"],
                    data["student_number"],
                ),
            )
            return "", 200

        else:
            error_messgae = f"Not allowed method"
            return render_template("error.html", data=error_messgae), 422


# FIXME: @random6 What is the purpose of this function???
# show and modify checkout history
@app.route("/admin/checkout", methods=["GET", "POST"])
def admin_checkout():
    result = check_admin(True if request.cookies.get("session") else False)
    if result != True:
        return result

    # show checkout history
    if request.method == "GET":
        result = Database().execute(
            "SELECT student_number, title, return, time FROM checkout_history"
        )
        return render_template("admin/checkout.html", data=result), 200

    # modify checkout history
    elif request.method == "POST":
        data = request.get_json()
        result = check_parameters(data, ["title", "return"])
        if result != True:
            return result

        Database().execute(
            "UPDATE checkout_history SET return=? WHERE title=?",
            [data["title"], data["return"]],
        )

        return "", 200


# process xlsx to list
def process_xlsx(file_name):
    xlsx = read_excel("./upload/" + file_name, "Sheet1")
    book_list = []

    for _, row in xlsx.iterrows():
        book_list.append(
            [
                row["책 제목"],
                row["지은이"],
                row["출판사"],
                row["수량"],
                1 if row["대출여부"] == "가능" else 0,
                row["분야"],
            ]
        )

    return book_list


# upload .xlsx file
@app.route("/admin/books/upload", methods=["GET", "POST"])
def admin_upload_books():
    result = check_admin(request.cookies.get("session"))
    if result != True:
        return result

    if request.method == "POST":
        # save xlsx
        if "file" not in request.files:
            error_message = "No file"
            return render_template("error.html", data=error_message), 422

        file = request.files["file"]
        if file.filename == "":
            error_message = "No selected file"
            return render_template("erorr.html", data=error_message), 422

        if not file:
            error_message = "empty file"
            return render_template("erorr.html", data=error_message), 422

        filename = secure_filename(file.filename)
        file.save("./upload/" + filename + ".xlsx")

        # append data to database
        xlsx = process_xlsx(filename + ".xlsx")
        book_info = [(data[:-1], data[-1]) for data in xlsx]
        db = Database()
        for row in book_info:
            id = db.execute(
                "INSERT INTO userbooks (title, writer, publisher, amount, available) VALUES (?, ?, ?, ?, ?)",
                row[0],
            )
            for category in row[1].split(","):
                db.execute(
                    "INSERT INTO book_field (book_id, category) VALUES (?, ?)",
                    (id, category.strip()),
                )

        return render_template("admin/upload_success.html"), 200

    elif request.method == "GET":
        return render_template("admin/upload.html"), 200


# TODO: @imStillDebugging admin show users
@app.route("/admin/users", methods=["GET"])
def admin_show_users():
    return


# TODO: @imStillDebugging admin modify users
@app.route("/admin/users/modify", methods=["POST"])
def admin_modify_users():
    return
