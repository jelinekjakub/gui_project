from flask import Flask
from extensions.env import Config
from app.routes import bp

# App init
app = Flask(__name__)
app.secret_key = Config().get("APP_KEY")

app.register_blueprint(bp)
if __name__ == '__main__':
    app.run(debug=False, host=Config().get("APP_HOST", "0.0.0.0"), port=Config().get("APP_PORT", 5000))
