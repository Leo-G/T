from flask import Flask

# http://flask.pocoo.org/docs/0.10/patterns/appfactories/


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from app.basemodels import db
    db.init_app(app)

    # Blueprints
    from app.roles.views import roles
    app.register_blueprint(roles, url_prefix='/api/v1/roles')
    from app.languages.views import languages
    app.register_blueprint(languages, url_prefix='/api/v1/languages')
    from app.users.views import users
    app.register_blueprint(users, url_prefix='/api/v1/users')
    from app.baseviews import login
    app.register_blueprint(login, url_prefix='/api/v1/login')

    return app
