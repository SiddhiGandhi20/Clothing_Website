from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.jacket_set_model import JacketSetModel

# Blueprint setup
jacket_set_bp = Blueprint("jacket_set", __name__)
UPLOAD_FOLDER = "uploads/jacket_sets/"  # Define folder for Jacket Set images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_jacket_set_routes(db):
    jacket_set_model = JacketSetModel(db)

    @jacket_set_bp.route("/jacket_sets", methods=["POST"])
    def create_jacket_set():
        """API endpoint to create a new Jacket Set item with an image."""
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.files.get("image")

        if not (name and price and image):
            return jsonify({"error": "Name, price, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        # Save the image securely
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # Save data to the database
        jacket_set_model.create_item(name, price, image_path)
        return jsonify({"message": "Jacket Set item created successfully"}), 201

    @jacket_set_bp.route("/jacket_sets", methods=["GET"])
    def get_jacket_sets():
        """API endpoint to fetch all Jacket Set items."""
        items = jacket_set_model.get_all_items()
        return jsonify(items), 200

    @jacket_set_bp.route("/jacket_sets/<item_id>", methods=["PUT"])
    def update_jacket_set(item_id):
        """API endpoint to update a Jacket Set item."""
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
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            update_data["image"] = image_path

        updated = jacket_set_model.update_item(item_id, update_data)
        if not updated:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Jacket Set item updated successfully"}), 200

    @jacket_set_bp.route("/jacket_sets/<item_id>", methods=["DELETE"])
    def delete_jacket_set(item_id):
        """API endpoint to delete a Jacket Set item."""
        deleted = jacket_set_model.delete_item(item_id)
        if not deleted:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Jacket Set item deleted successfully"}), 200

    return jacket_set_bp
