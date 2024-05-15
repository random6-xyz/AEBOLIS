from flask import render_template, request, jsonify
from modules import app
from databases.db import Database
import hashlib
import bcrypt
import json
from flask_login import UserMixin


# API : return sign up page
@app.route("/signup")
def show_sign_up_page():
    return render_template("signup.html")


# API : sign up (name, number, password) sha512 + salt
@app.route("/signup", methods=["POST"])
def sign_up():
    username = request.form["username"]
    student_id = int(request.form["student_id"])
    password = request.form["password"]

    row = Database().select_account_info(student_id)

    if row is not None:
        return jsonify({"message": "이미 사용 중인 학번입니다."}), 409
    elif not (8 <= password <= 30):
        return jsonify({"message": "비밀번호는 8자 이상 30자 이하이어야 합니다."}), 400
    else:
        salt = bcrypt.gensalt()
        hashed_password = hash_password(password, salt)
        Database().insert_account_info(
            student_id, username, hashed_password, salt, None
        )


def get_user_info(session):
    if session == True:
        info = {"role": "admin", "code": "11111111"}
    else:
        info = {"role": "user", "code": "22222222"}
    return info


# API : sign in, create session
# API : sign out, delete session
# API : delete account
# API : check session

################# NON API #######################


class User(UserMixin):
    def __init__(self, id, email, name, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"USER: {self.id} = {self.name}"


# hashing password
def hash_password(origin_password: str, salt):
    hash_input = (origin_password + salt).encode()
    hash_object = hashlib.sha512()
    hash_object.update(hash_input)
    return hash_object.hexdigest()


# check character
def is_ascii_33_to_126(string: str) -> bool:
    return all(("!" <= character <= "~") for character in string)
