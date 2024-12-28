from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.sherwani_model import SherwaniModel

# Blueprint setup
sherwani_bp = Blueprint("sherwani", __name__)
UPLOAD_FOLDER = "uploads/sherwanis/"  # Define folder for Sherwani images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_sherwani_routes(db):
    sherwani_model = SherwaniModel(db)

    @sherwani_bp.route("/sherwanis", methods=["POST"])
    def create_sherwani():
        """API endpoint to create a new Sherwani item with an image."""
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
        sherwani_model.create_item(name, price, image_path)
        return jsonify({"message": "Sherwani item created successfully"}), 201

    @sherwani_bp.route("/sherwanis", methods=["GET"])
    def get_sherwanis():
        """API endpoint to fetch all Sherwani items."""
        items = sherwani_model.get_all_items()
        return jsonify(items), 200

    @sherwani_bp.route("/sherwanis/<item_id>", methods=["PUT"])
    def update_sherwani(item_id):
        """API endpoint to update a Sherwani item."""
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

        updated = sherwani_model.update_item(item_id, update_data)
        if not updated:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Sherwani item updated successfully"}), 200

    @sherwani_bp.route("/sherwanis/<item_id>", methods=["DELETE"])
    def delete_sherwani(item_id):
        """API endpoint to delete a Sherwani item."""
        deleted = sherwani_model.delete_item(item_id)
        if not deleted:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Sherwani item deleted successfully"}), 200

    return sherwani_bp
