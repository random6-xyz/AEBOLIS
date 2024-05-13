from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder="../templates")
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SESSION_PERMANENT'] = False
app.secret_key = 'vjRP_TiR5EgnrExRI3QxRg'

import modules.user
import modules.auth
import modules.admin