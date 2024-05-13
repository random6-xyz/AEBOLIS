from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder="../templates")


import modules.user
import modules.auth
import modules.admin
