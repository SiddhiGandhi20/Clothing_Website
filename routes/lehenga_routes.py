import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from models.lehenga_model import LehengaModel

lehenga_bp = Blueprint("lehenga", __name__)

# Define Lehenga Upload Folder
LEHENGA_UPLOAD_FOLDER = "uploads/lehenga"
os.makedirs(LEHENGA_UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

def create_lehenga_routes(db):
    lehenga_model = LehengaModel(db)

    @lehenga_bp.route("/lehenga", methods=["GET"])
    def get_all_lehengas():
        """Get all lehengas."""
        lehengas = lehenga_model.get_all_lehengas()
        return jsonify(lehengas), 200

    @lehenga_bp.route("/lehenga/<string:lehenga_id>", methods=["GET"])
    def get_lehenga_by_id(lehenga_id):
        """Get a specific lehenga by ID."""
        lehenga = lehenga_model.get_lehenga_by_id(lehenga_id)
        if lehenga:
            return jsonify(lehenga), 200
        return jsonify({"error": "Lehenga not found"}), 404

    @lehenga_bp.route("/lehenga", methods=["POST"])
    def create_lehenga():
        """Add a new lehenga."""
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.files.get("image")

        if not (name and price and image):
            return jsonify({"error": "All fields are required"}), 400

        # Save image in the lehenga folder
        filename = secure_filename(image.filename)
        image_path = os.path.join(LEHENGA_UPLOAD_FOLDER, filename)  # Correct lehenga folder
        image.save(image_path)

        lehenga_id = lehenga_model.create_lehenga(name, price, image_path)
        return jsonify({"message": "Lehenga created", "id": lehenga_id}), 201

    @lehenga_bp.route("/lehenga/<string:lehenga_id>", methods=["PUT"])
    def update_lehenga(lehenga_id):
        """Update a lehenga."""
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.files.get("image")

        if not (name and price and image):
            return jsonify({"error": "All fields are required"}), 400

        # Save updated image in the lehenga folder
        filename = secure_filename(image.filename)
        image_path = os.path.join(LEHENGA_UPLOAD_FOLDER, filename)  # Correct lehenga folder
        image.save(image_path)

        updated = lehenga_model.update_lehenga(lehenga_id, name, price, image_path)
        if updated:
            return jsonify({"message": "Lehenga updated"}), 200
        return jsonify({"error": "Lehenga not found"}), 404

    @lehenga_bp.route("/lehenga/<string:lehenga_id>", methods=["DELETE"])
    def delete_lehenga(lehenga_id):
        """Delete a lehenga."""
        deleted = lehenga_model.delete_lehenga(lehenga_id)
        if deleted:
            return jsonify({"message": "Lehenga deleted"}), 200
        return jsonify({"error": "Lehenga not found"}), 404

    return lehenga_bp
