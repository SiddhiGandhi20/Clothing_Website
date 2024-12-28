from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from routes.admin_routes import setup_admin_routes
from routes.user_signup_routes import create_auth_routes
from routes.user_login_routes import setup_login_routes
from routes.bridal_wear_routes import create_bridal_wear_routes
from routes.lehenga_routes import create_lehenga_routes
from routes.sarees_routes import create_sarees_routes
from routes.coord_sets_routes import create_coord_sets_routes
from routes.sherwani_routes import create_sherwani_routes
from routes.kurta_set_routes import create_kurta_set_routes
from routes.blazer_set_routes import create_blazer_set_routes
from routes.jacket_set_routes import create_jacket_set_routes


from utils import JSONEncoder
import os

app = Flask(__name__)

# Load MongoDB configuration from the Config class
app.config.from_object(Config)

# Create the upload folder if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Initialize MongoDB connection
mongo = PyMongo(app)

# Set custom JSON encoder to handle MongoDB ObjectId
app.json_encoder = JSONEncoder

# Register blueprints
admin_bp = setup_admin_routes(mongo.db)
app.register_blueprint(admin_bp, url_prefix="/admin")

# User signup and login routes
auth_bp = create_auth_routes(mongo.db)
app.register_blueprint(auth_bp, url_prefix="/auth")

login_bp = setup_login_routes(mongo.db)
app.register_blueprint(login_bp, url_prefix="/auth")

bridal_wear_bp = create_bridal_wear_routes(mongo.db)
app.register_blueprint(bridal_wear_bp, url_prefix="/api")

# Lehenga routes
lehenga_bp = create_lehenga_routes(mongo.db)  # Pass the upload folder
app.register_blueprint(lehenga_bp, url_prefix="/api")

sarees_bp = create_sarees_routes(mongo.db)
app.register_blueprint(sarees_bp, url_prefix="/api")

coord_sets_bp = create_coord_sets_routes(mongo.db)
app.register_blueprint(coord_sets_bp, url_prefix="/api")

sherwani_bp = create_sherwani_routes(mongo.db)
app.register_blueprint(sherwani_bp, url_prefix="/api")

kurta_set_bp = create_kurta_set_routes(mongo.db)
app.register_blueprint(kurta_set_bp, url_prefix="/api")

blazer_set_bp = create_blazer_set_routes(mongo.db)
app.register_blueprint(blazer_set_bp, url_prefix="/api")

jacket_set_bp = create_jacket_set_routes(mongo.db)
app.register_blueprint(jacket_set_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Ensure the port is specified
