from bson import ObjectId

class CoordSetDetailModel:
    def __init__(self, db):
        self.collection = db.coordset_details

    def create_detail(self, name, description, image, price, coordset_id):
        """Insert a new coordset detail into the database."""
        detail_data = {
            "name": name,
            "description": description,
            "image": image,
            "price": price,
            "coordset_id": ObjectId(coordset_id)
        }
        self.collection.insert_one(detail_data)

    def get_detail_by_id(self, detail_id):
        """Retrieve a coordset detail by its ID."""
        detail = self.collection.find_one({"_id": ObjectId(detail_id)})
        if detail:
            return {
                "id": str(detail["_id"]),
                "name": detail["name"],
                "description": detail["description"],
                "image": detail["image"],
                "price": detail["price"],
                "coordset_id": str(detail["coordset_id"])
            }
        return None

    def update_detail(self, detail_id, update_data):
        """Update a coordset detail."""
        result = self.collection.update_one(
            {"_id": ObjectId(detail_id)},
            {"$set": update_data}
        )
        return result.matched_count > 0

    def delete_detail(self, detail_id):
        """Delete a coordset detail."""
        result = self.collection.delete_one({"_id": ObjectId(detail_id)})
        return result.deleted_count > 0
