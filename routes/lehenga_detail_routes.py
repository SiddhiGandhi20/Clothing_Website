from flask import Blueprint, request, jsonify, send_from_directory
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.lehenga_detail_model import LehengaDetailModel

lehenga_detail_bp = Blueprint("lehenga_detail", __name__)

UPLOAD_FOLDER = "uploads/lehengas_wear_details/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_lehenga_detail_routes(db):
    lehenga_detail_model = LehengaDetailModel(db)


    # Create a new blazerset wear detail
    @lehenga_detail_bp.route("/lehenga_detail", methods=["POST"])
    def create_lehenga_detail():
        """Create a new lehenga wear detail."""
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        lehenga_id = request.form.get("lehenga_id")
        image = request.files.get("image")

        if not (name and description and price and lehenga_id and image):
            return jsonify({"error": "Name, description, price, blazerset ID, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # Save relative path to the database
        relative_path = f"{UPLOAD_FOLDER}{filename}"

        inserted_id = lehenga_detail_model.create_item(
            name, description, relative_path, price, lehenga_id
        )
        if not inserted_id:
            return jsonify({"error": "Failed to create lehenga wear detail"}), 500

        return jsonify({"message": "lehenga wear detail created successfully", "id": inserted_id}), 201

    # Get a specific blazerset wear detail by ID
    @lehenga_detail_bp.route("/lehenga_detail/<detail_id>", methods=["GET"])
    def get_lehenga_detail(detail_id):
        """Fetch a lehenga wear detail by ID."""
        detail = lehenga_detail_model.get_item_by_id(detail_id)
        if not detail:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify(detail), 200

    # Update an existing blazerset wear detail
    @lehenga_detail_bp.route("/lehenga_detail/<detail_id>", methods=["PUT"])
    def update_lehenga_detail(detail_id):
        """Update a lehenga wear detail."""
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
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            update_data["image"] = f"{UPLOAD_FOLDER}{filename}"

        updated = lehenga_detail_model.update_item(detail_id, update_data)
        if not updated:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "blazerset wear detail updated successfully"}), 200

    # Delete a specific blazerset wear detail
    @lehenga_detail_bp.route("/lehenga_detail/<detail_id>", methods=["DELETE"])
    def delete_lehenga_detail(detail_id):
        """Delete a lehenga wear detail."""
        deleted = lehenga_detail_model.delete_item(detail_id)
        if not deleted:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "lehenga wear detail deleted successfully"}), 200
    
    @lehenga_detail_bp.route("/uploads/lehengas_wear_details/<filename>")
    def serve_image(filename):
        try:
            return send_from_directory(UPLOAD_FOLDER, filename)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404


    return lehenga_detail_bp
