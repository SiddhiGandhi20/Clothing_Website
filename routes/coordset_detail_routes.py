from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.coordset_detail_model import CoordSetDetailModel

coordset_detail_bp = Blueprint("coordset_detail", __name__)
UPLOAD_FOLDER = "uploads/coordsets_wear_details/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_coordset_detail_routes(db, upload_folder=UPLOAD_FOLDER):
    coordset_detail_model = CoordSetDetailModel(db)

    @coordset_detail_bp .route("/coordset_detail", methods=["POST"])
    def create_coordset_detail():
        """Create a new coordsets wear detail."""
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        coordset_id = request.form.get("coordset_id")
        image = request.files.get("image")

        if not (name and description and price and coordset_id and image):
            return jsonify({"error": "Name, description, price, coordsets wear ID, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        coordset_detail_model.create_detail(name, description, image_path, price, coordset_id)
        return jsonify({"message": "coordsets wear detail created successfully"}), 201

    @coordset_detail_bp .route("/coordset_detail/<detail_id>", methods=["GET"])
    def get_coordset_detail(detail_id):
        """Fetch a coordsets wear detail by ID."""
        detail = coordset_detail_model.get_detail_by_id(detail_id)
        if not detail:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify(detail), 200

    @coordset_detail_bp .route("/coordset_detail/<detail_id>", methods=["PUT"])
    def update_coordset_detail(detail_id):
        """Update a coordsets wear detail."""
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

        updated = coordset_detail_model.update_detail(detail_id, update_data)
        if not updated:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "coordset wear detail updated successfully"}), 200

    @coordset_detail_bp .route("/coordset_detail/<detail_id>", methods=["DELETE"])
    def delete_coordset_detail(detail_id):
        """Delete a coordsets wear detail."""
        deleted = coordset_detail_model.delete_detail(detail_id)
        if not deleted:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "coordsets wear detail deleted successfully"}), 200

    return coordset_detail_bp 
