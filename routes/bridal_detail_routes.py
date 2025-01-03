from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.bridal_detail_model import BridalWearDetailModel

bridalwear_detail_bp = Blueprint("bridalwear_detail", __name__)
UPLOAD_FOLDER = "uploads/bridal_wear_details/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_bridalwear_detail_routes(db, upload_folder=UPLOAD_FOLDER):
    bridalwear_detail_model = BridalWearDetailModel(db)

    @bridalwear_detail_bp.route("/bridalwear_detail", methods=["POST"])
    def create_bridalwear_detail():
        """Create a new bridal wear detail."""
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        bridal_wear_id = request.form.get("bridal_wear_id")
        image = request.files.get("image")

        if not (name and description and price and bridal_wear_id and image):
            return jsonify({"error": "Name, description, price, bridal wear ID, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        bridalwear_detail_model.create_detail(name, description, image_path, price, bridal_wear_id)
        return jsonify({"message": "Bridal wear detail created successfully"}), 201

    @bridalwear_detail_bp.route("/bridalwear_detail/<detail_id>", methods=["GET"])
    def get_bridalwear_detail(detail_id):
        """Fetch a bridal wear detail by ID."""
        detail = bridalwear_detail_model.get_detail_by_id(detail_id)
        if not detail:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify(detail), 200

    @bridalwear_detail_bp.route("/bridalwear_detail/<detail_id>", methods=["PUT"])
    def update_bridalwear_detail(detail_id):
        """Update a bridal wear detail."""
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        image = request.files.get("image")

        update_data = {}
        if name:
            update_data["name"] = name
        if description:
            update_data["description"] = description
        if price:
            update_data["price"] = price

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            update_data["image"] = image_path

        updated = bridalwear_detail_model.update_detail(detail_id, update_data)
        if not updated:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "Bridal wear detail updated successfully"}), 200

    @bridalwear_detail_bp.route("/bridalwear_detail/<detail_id>", methods=["DELETE"])
    def delete_bridalwear_detail(detail_id):
        """Delete a bridal wear detail."""
        deleted = bridalwear_detail_model.delete_detail(detail_id)
        if not deleted:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "Bridal wear detail deleted successfully"}), 200

    return bridalwear_detail_bp
