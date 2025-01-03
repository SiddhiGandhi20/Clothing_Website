from bson import ObjectId

class SareeDetailModel:
    def __init__(self, db):
        self.collection = db.saree_details

    def create_detail(self, name, description, image, price, saree_id):
        """Insert a new saree detail into the database."""
        detail_data = {
            "name": name,
            "description": description,
            "image": image,
            "price": price,
            "saree_id": ObjectId(saree_id)
        }
        self.collection.insert_one(detail_data)

    def get_detail_by_id(self, detail_id):
        """Retrieve a saree detail by its ID."""
        detail = self.collection.find_one({"_id": ObjectId(detail_id)})
        if detail:
            return {
                "id": str(detail["_id"]),
                "name": detail["name"],
                "description": detail["description"],
                "image": detail["image"],
                "price": detail["price"],
                "saree_id": str(detail["saree_id"])
            }
        return None

    def update_detail(self, detail_id, update_data):
        """Update a saree detail."""
        result = self.collection.update_one(
            {"_id": ObjectId(detail_id)},
            {"$set": update_data}
        )
        return result.matched_count > 0

    def delete_detail(self, detail_id):
        """Delete a saree detail."""
        result = self.collection.delete_one({"_id": ObjectId(detail_id)})
        return result.deleted_count > 0
