from flask import Blueprint, request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.lehenga_detail_model import LehengaDetailModel

lehenga_detail_bp = Blueprint("lehenga_detail", __name__)
UPLOAD_FOLDER = "uploads/lehengas_wear_details/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_lehenga_detail_routes(db, upload_folder=UPLOAD_FOLDER):
    lehenga_detail_model = LehengaDetailModel(db)

    @lehenga_detail_bp .route("/lehenga_detail", methods=["POST"])
    def create_lehenga_detail():
        """Create a new lehengas wear detail."""
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        lehenga_id = request.form.get("lehenga_id")
        image = request.files.get("image")

        if not (name and description and price and lehenga_id and image):
            return jsonify({"error": "Name, description, price, lehengas wear ID, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        filename = secure_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        lehenga_detail_model.create_detail(name, description, image_path, price, lehenga_id)
        return jsonify({"message": "lehengas wear detail created successfully"}), 201

    @lehenga_detail_bp .route("/lehenga_detail/<detail_id>", methods=["GET"])
    def get_lehenga_detail(detail_id):
        """Fetch a lehengas wear detail by ID."""
        detail = lehenga_detail_model.get_detail_by_id(detail_id)
        if not detail:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify(detail), 200

    @lehenga_detail_bp .route("/lehenga_detail/<detail_id>", methods=["PUT"])
    def update_lehenga_detail(detail_id):
        """Update a lehengas wear detail."""
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

        updated = lehenga_detail_model.update_detail(detail_id, update_data)
        if not updated:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "lehenga wear detail updated successfully"}), 200

    @lehenga_detail_bp .route("/lehenga_detail/<detail_id>", methods=["DELETE"])
    def delete_lehenga_detail(detail_id):
        """Delete a lehengas wear detail."""
        deleted = lehenga_detail_model.delete_detail(detail_id)
        if not deleted:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "lehengas wear detail deleted successfully"}), 200

    return lehenga_detail_bp 
