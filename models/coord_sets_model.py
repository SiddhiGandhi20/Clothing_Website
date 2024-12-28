from bson import ObjectId

class CoordSetModel:
    def __init__(self, db):
        self.collection = db.coord_sets

    def create_item(self, name, price, image):
        """Insert a new Co-Ord Set item into the database."""
        item_data = {
            "name": name,
            "price": price,
            "image": image
        }
        self.collection.insert_one(item_data)

    def get_all_items(self):
        """Retrieve all Co-Ord Set items."""
        items = self.collection.find()
        return [
            {
                "id": str(item["_id"]),
                "name": item["name"],
                "price": item["price"],
                "image": item["image"]
            } for item in items
        ]

    def update_item(self, item_id, update_data):
        """Update a Co-Ord Set item."""
        result = self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        return result.matched_count > 0

    def delete_item(self, item_id):
        """Delete a Co-Ord Set item."""
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0