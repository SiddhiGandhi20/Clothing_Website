from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.bridal_wear_model import BridalWearModel

# Blueprint setup
bridal_wear_bp = Blueprint("bridal_wear", __name__)
UPLOAD_FOLDER = "uploads/bridal_wear/"  # Correct folder name
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_bridal_wear_routes(db, upload_folder=UPLOAD_FOLDER):
    bridal_wear_model = BridalWearModel(db)

    @bridal_wear_bp.route("/bridal_wear", methods=["POST"])
    def create_bridal_wear():
        """Create a new bridal wear item with an image."""
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.files.get("image")

        if not (name and price and image):
            return jsonify({"error": "Name, price, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        # Save the image securely
        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        # Save to the database
        bridal_wear_model.create_item(name, price, image_path)
        return jsonify({"message": "Bridal wear item created successfully"}), 201

    @bridal_wear_bp.route("/bridal_wear", methods=["GET"])
    def get_bridal_wear():
        """Fetch all bridal wear items."""
        items = bridal_wear_model.get_all_items()
        return jsonify(items), 200

    @bridal_wear_bp.route("/bridal_wear/<item_id>", methods=["PUT"])
    def update_bridal_wear(item_id):
        """Update a bridal wear item."""
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.files.get("image")

        update_data = {}
        if name:
            update_data["name"] = name
        if price:
            update_data["price"] = price

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            update_data["image"] = image_path

        updated = bridal_wear_model.update_item(item_id, update_data)
        if not updated:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Bridal wear item updated successfully"}), 200

    @bridal_wear_bp.route("/bridal_wear/<item_id>", methods=["DELETE"])
    def delete_bridal_wear(item_id):
        """Delete a bridal wear item."""
        deleted = bridal_wear_model.delete_item(item_id)
        if not deleted:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Bridal wear item deleted successfully"}), 200

    return bridal_wear_bp
