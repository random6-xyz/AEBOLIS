from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder="../templates")
# login_manager = LoginManager()
# login_manager.init_app(app)

import modules.user
import modules.auth
import modules.admin
