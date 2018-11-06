from flask import Flask
from pages import site

app = Flask(__name__)

app.register_blueprint(site)


if __name__ == '__main__':
    port = app.config.get("PORT", 5000)
    debug = True
    app.run(host='0.0.0.0', port=port, debug=debug)
