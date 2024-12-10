from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Đảm bảo đường dẫn tới cơ sở dữ liệu là chính xác
    import os

# Lưu SQLite trong thư mục tạm thời của Vercel
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'ebook.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .routes_admin import api_admin
    app.register_blueprint(api_admin, url_prefix='/api/admin')

    return app
