from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.jacketset_detail_model import JacketSetDetailModel

jacketset_detail_bp = Blueprint("jacketset_detail", __name__)
UPLOAD_FOLDER = "uploads/jacketsets_wear_details/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_jacketset_detail_routes(db, upload_folder=UPLOAD_FOLDER):
    jacketset_detail_model = JacketSetDetailModel(db)

    @jacketset_detail_bp .route("/jacketset_detail", methods=["POST"])
    def create_jacketset_detail():
        """Create a new jacketsets wear detail."""
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        jacketset_id = request.form.get("jacketset_id")
        image = request.files.get("image")

        if not (name and description and price and jacketset_id and image):
            return jsonify({"error": "Name, description, price, jacketsets wear ID, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        jacketset_detail_model.create_detail(name, description, image_path, price, jacketset_id)
        return jsonify({"message": "jacketsets wear detail created successfully"}), 201

    @jacketset_detail_bp .route("/jacketset_detail/<detail_id>", methods=["GET"])
    def get_jacketset_detail(detail_id):
        """Fetch a jacketsets wear detail by ID."""
        detail = jacketset_detail_model.get_detail_by_id(detail_id)
        if not detail:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify(detail), 200

    @jacketset_detail_bp .route("/jacketset_detail/<detail_id>", methods=["PUT"])
    def update_jacketset_detail(detail_id):
        """Update a jacketsets wear detail."""
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

        updated = jacketset_detail_model.update_detail(detail_id, update_data)
        if not updated:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "jacketset wear detail updated successfully"}), 200

    @jacketset_detail_bp .route("/jacketset_detail/<detail_id>", methods=["DELETE"])
    def delete_jacketset_detail(detail_id):
        """Delete a jacketsets wear detail."""
        deleted = jacketset_detail_model.delete_detail(detail_id)
        if not deleted:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "jacketsets wear detail deleted successfully"}), 200

    return jacketset_detail_bp 
