from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
from .api.chat import chat_bp
from .api.group import group_bp
from .api.user import user_bp
from .api.system import system_bp
from .api.auth import auth_bp
from .models.database import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:9528"}})

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(group_bp, url_prefix='/api/group')
    app.register_blueprint(system_bp, url_prefix='/api')
    app.register_blueprint(auth_bp,url_prefix='/api/login')
    app.register_blueprint(user_bp,url_prefix='/api/user')

    return app
