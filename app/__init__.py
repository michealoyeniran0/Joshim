from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask import Flask,render_template
from flask_login import LoginManager
from config import Config
from app.models import db,User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load configuration
    app.config.from_object(Config)
    
    csrf.init_app(app)

    # Initialize database
    db.init_app(app)

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"

    #Initiate mail
    mail.init_app(app)

    limiter.init_app(app)

    # Import routes
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.admin import admin_bp
    from app.routes.payment import payment_bp

      # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payment_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"),404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("500.html"),500

    return app