from flask_cors import CORS
from app import create_app
app = create_app()
CORS(app)  # Cho phép tất cả các nguồn truy cập API

if __name__ == "__main__":
    app.run(debug=True)
