from flask import Flask
import pages

def create_app():
    app = Flask(__name__)
    #app.config.from_object("settings")
    app.add_url_rule("/initdb", view_func=pages.initialize_database)
    app.add_url_rule("/", view_func=pages.home_page)
    app.add_url_rule("/index", view_func=pages.home_page)
    app.add_url_rule("/login", view_func=pages.login_page)

    return app

if __name__ == '__main__':
    app = create_app()
    port = app.config.get("PORT", 5000)
    debug = True
    app.run(host='0.0.0.0', port=port, debug=debug)
