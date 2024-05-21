from flask import render_template, request, jsonify, session, redirect, url_for
from flask_login import (
    UserMixin,
    login_manager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from setting.setup import app, login_manager
from databases.db import Database
import hashlib
import bcrypt
from setting.setup import access_logger, signup_logger


##################### API ##############################


# API : sign up (name, number, password) sha512 + salt
@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        # get user information from form data
        username = request.form["username"]
        student_id = int(request.form["student_id"])
        password = request.form["password"]

        # srearch user data from database
        row = Database().select_account_info(student_id)

        if row is not None:
            write_signup_log("invalid signup request", student_id)
            return jsonify({"message": "이미 사용 중인 학번입니다."}), 400
        elif not (8 <= len(password) <= 30):
            write_signup_log("invalid signup request", student_id)
            return (
                jsonify({"message": "비밀번호는 8자 이상 30자 이하이어야 합니다."}),
                400,
            )
        elif not is_ascii_33_to_126(password):
            write_signup_log("invalid signup request", student_id)
            return (
                jsonify(
                    {"message": "비밀번호에 사용할 수 없는 문자가 포함되어 있습니다."}
                ),
                400,
            )
        else:
            # if user information is valid for sign-up
            salt = (bcrypt.gensalt()).decode("utf-8")
            hashed_password = hash_password(password, salt)
            Database().insert_account_info(
                student_id, username, hashed_password, salt, None
            )
            write_signup_log("Successful request for Signup", student_id)
            return redirect(url_for("index"))

    return render_template("signup.html")


# API : sign in, create session
@app.route("/signin", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        student_id = int(request.form["student_id"])
        password = request.form["password"]
        row = Database().select_account_info(student_id)
        if (
            (row is not None)
            and (hash_password(password, row[3]) == row[2])
            and (not row[4])
            and row[5]
        ):
            user = User(row)
            login_user(user)
            write_access_log("Signin successed", student_id)
            return redirect(url_for("index"))
        write_access_log("Signin failed", student_id)
        return jsonify({"message": "계정 정보가 올바르지 않습니다."}), 403

    return render_template("signin.html")


# API : sign out, delete session
@app.route("/signout", methods=["POST", "GET"])
@login_required
def sign_out():
    if request.method == "POST":
        write_access_log("Signout successed", current_user.get_id())
        logout_user()
        return redirect(url_for("index"))
    return render_template("signout.html")


# API : delete account
@app.route("/delete_account", methods=["POST", "GET"])
@login_required
def delete_account():
    if request.method == "POST":
        password = request.form["password"]
        row = Database().select_account_info(current_user.get_id())

        if (
            (row is not None)
            and (hash_password(password, row[3]) == row[2])
            and (not row[4])
            and row[5]
        ):
            logout_user()
            Database().delete_user(row[0])
            write_signup_log("deleted acount successful", row[0])
            write_access_log("Logout Occurs Due to Account Deletion", row[0])
            return redirect(url_for("index"))
        return jsonify({"message": "올바르지 않은 계정 정보입니다."}), 400

    return render_template("delete_account.html")


################# NON API #######################


class User(UserMixin):
    def __init__(self, row: tuple):
        self.__id = row[0]
        self.__name = row[1]
        self.__role = bool(row[4])

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_role(self):
        return self.__role

    def __repr__(self):
        return f"USER: {self.__id} = {self.__name}"

    def get_user_dict(self):
        return {"id": self.__id, "name": self.__name, "role": self.__role}


# hashing password
def hash_password(origin_password: str, salt):
    hash_input = (origin_password + salt).encode()
    hash_object = hashlib.sha512()
    hash_object.update(hash_input)
    return hash_object.hexdigest()


# check character
def is_ascii_33_to_126(string: str) -> bool:
    return all(("!" <= character <= "~") for character in string)


def get_user_info(session):
    return current_user.get_user_dict()


# get user informations from database
@login_manager.user_loader
def load_user(user_id: int) -> User:
    row = Database().select_account_info(user_id)
    if row is not None:
        return User(row)
    return None


def check_session():
    return bool(session.get("user_id"))


def write_access_log(head: str, student_id: int):
    access_logger.info(
        head,
        extra={
            "remote_addr": request.remote_addr,
            "id": student_id,
        },
    )


def write_signup_log(head: str, student_id: int):
    signup_logger.info(
        head,
        extra={
            "remote_addr": request.remote_addr,
            "id": student_id,
        },
    )
