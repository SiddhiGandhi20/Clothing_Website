from bson import ObjectId

class SherwaniDetailModel:
    def __init__(self, db):
        self.collection = db.sherwani_details

    def create_detail(self, name, description, image, price, sherwani_id):
        """Insert a new sherwani detail into the database."""
        detail_data = {
            "name": name,
            "description": description,
            "image": image,
            "price": price,
            "sherwani_id": ObjectId(sherwani_id)
        }
        self.collection.insert_one(detail_data)

    def get_detail_by_id(self, detail_id):
        """Retrieve a sherwani detail by its ID."""
        detail = self.collection.find_one({"_id": ObjectId(detail_id)})
        if detail:
            return {
                "id": str(detail["_id"]),
                "name": detail["name"],
                "description": detail["description"],
                "image": detail["image"],
                "price": detail["price"],
                "sherwani_id": str(detail["sherwani_id"])
            }
        return None

    def update_detail(self, detail_id, update_data):
        """Update a sherwani detail."""
        result = self.collection.update_one(
            {"_id": ObjectId(detail_id)},
            {"$set": update_data}
        )
        return result.matched_count > 0

    def delete_detail(self, detail_id):
        """Delete a sherwani detail."""
        result = self.collection.delete_one({"_id": ObjectId(detail_id)})
        return result.deleted_count > 0
