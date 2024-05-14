from flask import Flask

app = Flask(__name__, template_folder="../templates")


import modules.user
import modules.auth
import modules.admin
