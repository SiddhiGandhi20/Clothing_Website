from flask import Blueprint, request, jsonify, send_from_directory
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from models.blazerset_detail_model import BlazersetDetailModel

blazerset_detail_bp = Blueprint("blazerset_detail", __name__)

UPLOAD_FOLDER = "uploads/blazersets_wear_details/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_blazerset_detail_routes(db):
    blazerset_detail_model = BlazersetDetailModel(db)


    # Create a new blazerset wear detail
    @blazerset_detail_bp.route("/blazerset_detail", methods=["POST"])
    def create_blazerset_detail():
        """Create a new blazersets wear detail."""
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        blazerset_id = request.form.get("blazerset_id")
        image = request.files.get("image")

        if not (name and description and price and blazerset_id and image):
            return jsonify({"error": "Name, description, price, blazerset ID, and image are required"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # Save relative path to the database
        relative_path = f"{UPLOAD_FOLDER}{filename}"

        inserted_id = blazerset_detail_model.create_item(
            name, description, relative_path, price, blazerset_id
        )
        if not inserted_id:
            return jsonify({"error": "Failed to create blazersets wear detail"}), 500

        return jsonify({"message": "blazersets wear detail created successfully", "id": inserted_id}), 201

    # Get a specific blazerset wear detail by ID
    @blazerset_detail_bp.route("/blazerset_detail/<detail_id>", methods=["GET"])
    def get_blazerset_detail(detail_id):
        """Fetch a blazersets wear detail by ID."""
        detail = blazerset_detail_model.get_item_by_id(detail_id)
        if not detail:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify(detail), 200

    # Update an existing blazerset wear detail
    @blazerset_detail_bp.route("/blazerset_detail/<detail_id>", methods=["PUT"])
    def update_blazerset_detail(detail_id):
        """Update a blazersets wear detail."""
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

        updated = blazerset_detail_model.update_item(detail_id, update_data)
        if not updated:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "blazerset wear detail updated successfully"}), 200

    # Delete a specific blazerset wear detail
    @blazerset_detail_bp.route("/blazerset_detail/<detail_id>", methods=["DELETE"])
    def delete_blazerset_detail(detail_id):
        """Delete a blazersets wear detail."""
        deleted = blazerset_detail_model.delete_item(detail_id)
        if not deleted:
            return jsonify({"error": "Detail not found"}), 404

        return jsonify({"message": "blazersets wear detail deleted successfully"}), 200
    
    @blazerset_detail_bp.route("/uploads/blazersets_wear_details/<filename>")
    def serve_image(filename):
        try:
            return send_from_directory(UPLOAD_FOLDER, filename)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404


    return blazerset_detail_bp
