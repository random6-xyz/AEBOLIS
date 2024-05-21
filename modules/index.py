from flask import render_template
from modules import app
from databases.db import Database
from modules.auth import get_user_info
from flask_login import login_required


@app.route("/", methods=["GET"])
def index():
    result = Database().execute("SELECT category FROM category")
    return render_template("index.html", data=result), 200


@app.route("/admin", methods=["GET"])
@login_required
def admin_index():
    if get_user_info()["role"] != True:
        error_messgae = "Not authenticated, You are not admin"
        return render_template("error.html", data=error_messgae), 401
