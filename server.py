from flask import Flask
from pages import site
from flask_login import LoginManager
from login import LoginDatabase

app = Flask(__name__)

app.register_blueprint(site)
"""login_manager = LoginManager()


login_manager.init_app(app)
login_manager.login_view = 'site.login_page'"""

if __name__ == '__main__':
    port = app.config.get("PORT", 5000)
    debug = True
    app.run(host='0.0.0.0', port=port, debug=debug)
