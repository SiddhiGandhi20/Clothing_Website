from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from models.bridal_wear_model import BridalWearModel

# Blueprint setup
bridal_wear_bp = Blueprint("bridal_wear", __name__)

# Constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads/bridal_wear/")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_bridal_wear_routes(db, upload_folder=UPLOAD_FOLDER):
    """Factory function to create bridal wear routes."""
    bridal_wear_model = BridalWearModel(db)

    # Route: Create a new bridal wear item
    @bridal_wear_bp.route("/bridal_wear", methods=["POST"])
    def create_bridal_wear():
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.files.get("image")

        # Validate input
        if not (name and price and image):
            return jsonify({"error": "Name, price, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        # Save the image securely
        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        # Store relative path in the database
        relative_path = f"bridal_wear/{filename}"
        bridal_wear_model.create_item(name, price, relative_path)

        return jsonify({"message": "Bridal wear item created successfully"}), 201

    # Route: Fetch all bridal wear items
    @bridal_wear_bp.route("/bridal_wear", methods=["GET"])
    def get_bridal_wear():
        items = bridal_wear_model.get_all_items()

        # Assuming items are MongoDB documents, manually adding '_id' as string
        for item in items:
            if isinstance(item, dict) and "_id" in item:
                item["_id"] = str(item["_id"])  # Convert ObjectId to string for JSON serialization
            else:
                # Handle cases where '_id' might be missing or item is not a dict
                item["_id"] = None

        return jsonify(items), 200

    # Route: Update a bridal wear item
    @bridal_wear_bp.route("/bridal_wear/<item_id>", methods=["PUT"])
    def update_bridal_wear(item_id):
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.files.get("image")

        update_data = {}
        if name:
            update_data["name"] = name
        if price:
            update_data["price"] = price

        # If a new image is uploaded, save it
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            update_data["image"] = f"uploads/bridal_wear/{filename}"

        updated = bridal_wear_model.update_item(item_id, update_data)
        if not updated:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Bridal wear item updated successfully"}), 200

    # Route: Delete a bridal wear item
    @bridal_wear_bp.route("/bridal_wear/<item_id>", methods=["DELETE"])
    def delete_bridal_wear(item_id):
        deleted = bridal_wear_model.delete_item(item_id)
        if not deleted:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Bridal wear item deleted successfully"}), 200

    # Route: Serve uploaded images
    @bridal_wear_bp.route("/uploads/bridal_wear/<filename>")
    def serve_image(filename):
        try:
            return send_from_directory(upload_folder, filename)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404

    return bridal_wear_bp
