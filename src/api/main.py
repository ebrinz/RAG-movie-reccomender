from flask import Flask
from flask_cors import CORS
from routes import api_bp 

app = Flask(__name__)
CORS(app)  # Enable CORS if needed
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)