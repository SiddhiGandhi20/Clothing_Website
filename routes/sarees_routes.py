from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.saree_model import SareeModel

# Blueprint setup
sarees_bp = Blueprint("sarees", __name__)
UPLOAD_FOLDER = "uploads/sarees/"  # Define folder for Saree images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_sarees_routes(db):
    saree_model = SareeModel(db)

    @sarees_bp.route("/sarees", methods=["POST"])
    def create_saree():
        """API endpoint to create a new Saree item with an image."""
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
        saree_model.create_item(name, price, image_path)
        return jsonify({"message": "Saree item created successfully"}), 201

    @sarees_bp.route("/sarees", methods=["GET"])
    def get_sarees():
        """API endpoint to fetch all Saree items."""
        items = saree_model.get_all_items()
        return jsonify(items), 200

    @sarees_bp.route("/sarees/<item_id>", methods=["PUT"])
    def update_saree(item_id):
        """API endpoint to update a Saree item."""
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

        updated = saree_model.update_item(item_id, update_data)
        if not updated:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Saree item updated successfully"}), 200

    @sarees_bp.route("/sarees/<item_id>", methods=["DELETE"])
    def delete_saree(item_id):
        """API endpoint to delete a Saree item."""
        deleted = saree_model.delete_item(item_id)
        if not deleted:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Saree item deleted successfully"}), 200

    return sarees_bp
