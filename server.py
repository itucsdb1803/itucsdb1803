from flask import Flask
from pages import site
from flask_login import LoginManager
from login import *

app = Flask(__name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return LoginDatabase.select_login_info(user_id)

if __name__ == '__main__':

    app.config.from_object('settings')
    app.register_blueprint(site)
    login_manager.init_app(app)
    login_manager.login_view = 'site.login_page'

    port = app.config.get("PORT", 5000)
    debug = True
    app.run(host='0.0.0.0', port=port, debug=debug)