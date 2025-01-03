from bson import ObjectId

class BlazersetDetailModel:
    def __init__(self, db):
        self.collection = db.blazerset_details

    def create_detail(self, name, description, image, price, blazerset_id):
        """Insert a new blazerset detail into the database."""
        detail_data = {
            "name": name,
            "description": description,
            "image": image,
            "price": price,
            "blazerset_id": ObjectId(blazerset_id)
        }
        self.collection.insert_one(detail_data)

    def get_detail_by_id(self, detail_id):
        """Retrieve a blazerset detail by its ID."""
        detail = self.collection.find_one({"_id": ObjectId(detail_id)})
        if detail:
            return {
                "id": str(detail["_id"]),
                "name": detail["name"],
                "description": detail["description"],
                "image": detail["image"],
                "price": detail["price"],
                "blazerset_id": str(detail["blazerset_id"])
            }
        return None

    def update_detail(self, detail_id, update_data):
        """Update a blazerset detail."""
        result = self.collection.update_one(
            {"_id": ObjectId(detail_id)},
            {"$set": update_data}
        )
        return result.matched_count > 0

    def delete_detail(self, detail_id):
        """Delete a blazerset detail."""
        result = self.collection.delete_one({"_id": ObjectId(detail_id)})
        return result.deleted_count > 0
