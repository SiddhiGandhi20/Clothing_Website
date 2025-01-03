from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from models.lehenga_model import LehengaModel

# Blueprint setup
lehenga_bp = Blueprint("lehenga", __name__)

# Constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads/lehenga/")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_lehenga_routes(db, upload_folder=UPLOAD_FOLDER):
    """Factory function to create blazer routes."""
    lehenga_model = LehengaModel(db)

    # Route: Create a new Lehenga item
    @lehenga_bp.route("/lehenga", methods=["POST"])
    def create_lehenga():
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
        relative_path = f"lehenga/{filename}"
        lehenga_model.create_item(name, price, relative_path)

        return jsonify({"message": "Lehenga item created successfully"}), 201

    # Route: Fetch all Lehenga items
    @lehenga_bp.route("/lehenga", methods=["GET"])
    def get_lehenga():
        items = lehenga_model.get_all_items()  # Fetch items from the database

        base_url = request.host_url  # Get the base URL dynamically

        for item in items:
            # Convert `_id` to string for JSON serialization
            if "_id" in item and item["_id"]:
                item["_id"] = str(item["_id"])
            else:
                item["_id"] = None

            # Append full URL for image
            if "image_url" in item:
                item["image_url"] = base_url + item["image_url"]

        return jsonify(items), 200


    # Route: Update a Lehenga item
    @lehenga_bp.route("/lehenga/<item_id>", methods=["PUT"])
    def update_lehenga(item_id):
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
            update_data["image"] = f"uploads/lehenga/{filename}"

        updated = lehenga_model.update_item(item_id, update_data)
        if not updated:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Lehenga item updated successfully"}), 200

    # Route: Delete a Lehenga item
    @lehenga_bp.route("/lehenga/<item_id>", methods=["DELETE"])
    def delete_lehenga(item_id):
        deleted = lehenga_model.delete_item(item_id)
        if not deleted:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Lehenga item deleted successfully"}), 200

    # Route: Serve uploaded images
    @lehenga_bp.route("/uploads/lehenga/<filename>")
    def serve_image(filename):
        try:
            return send_from_directory(upload_folder, filename)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404

    return lehenga_bp
