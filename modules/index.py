from flask import render_template, send_from_directory
from flask_login import current_user
from modules import app
from databases.db import Database
from modules.auth import get_user_info
from flask_login import login_required
from os import path


@app.route("/", methods=["GET"])
def index():
    result = list(Database().execute("SELECT category FROM category"))

    if current_user.is_authenticated:
        result.append(True)
    else:
        result.append(False)
    return render_template("index.html", data=result), 200


@app.route("/admin", methods=["GET"])
@login_required
def admin_index():
    if get_user_info()["role"] != True:
        error_messgae = "Not authenticated, You are not admin"
        return render_template("error.html", data=error_messgae), 401

    return render_template("admin/index.html"), 200


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(path.join(app.root_path, "../static"), "favicon.ico")
