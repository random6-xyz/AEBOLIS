from flask import render_template, request
from modules import app
from databases.db import Database
from modules.auth import get_user_info
from pandas import read_excel
from werkzeug.utils import secure_filename


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


# add books
@app.route("/admin/books/add", methods=["POST"])
def admin_add_books():
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

    for field in data["field"]:
        Database().execute(
            "INSERT INTO book_field (book_id, category) VALUES (?, ?)",
            (
                book_id[0][0],
                field,
            ),
        )

    return "", 200


# modifying books for admin
@app.route("/admin/books/modify", methods=["POST"])
def admin_modify_books():
    data = request.get_json()
    result = check_parameters_admin(
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
        request.cookies.get("session"),
    )
    if result != True:
        return result

    # Update userbooks table
    Database().execute(
        "UPDATE userbooks SET available=?, title=?, writer=?, publisher=?, amount=? WHERE title=?",
        (
            data["available"],
            data["title"],
            data["writer"],
            data["publisher"],
            data["amount"],
            data["old_title"],
        ),
    )

    # Update book_field table
    id = Database().execute("SELECT id FROM userbooks WHERE title=?", (data["title"],))[
        0
    ][0]
    Database().execute("DELETE FROM book_field WHERE book_id=?", (id,))
    for category in data["category"]:
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

    Database().execute("DELETE FROM userbooks WHERE title=?", (data["title"],))

    return "", 200


# TODO: @random6 admin show logs
@app.route("/admin/logs", methods=["GET"])
def admin_logs():
    return


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


# TODO: @random6 upload .xlsx file
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
            error_message = "No file"
            return render_template("erorr.html", data=error_message), 422

        filename = secure_filename(file.filename)
        file.save("./upload/" + filename)

        # append data to database
        xlsx = process_xlsx(filename)
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
                
    return "", 200


# TODO: @imStillDebugging admin show users
@app.route("/admin/users", methods=["GET"])
def admin_show_users():
    return


# TODO: @imStillDebugging admin modify users
@app.route("/admin/users/modify", methods=["POST"])
def admin_modify_users():
    return
