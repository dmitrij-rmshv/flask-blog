from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_blog_app.config import Config
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    # print(f'---------\n<NAME> : {__name__}\n---------')
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from flask_blog_app.main.routes import main
    app.register_blueprint(main)
    from flask_blog_app.user_apl.routes import users
    app.register_blueprint(users)
    from flask_blog_app.blog_apl.routes import posts
    app.register_blueprint(posts)
    from flask_blog_app.errors.handlers import errors
    app.register_blueprint(errors)

    return app
