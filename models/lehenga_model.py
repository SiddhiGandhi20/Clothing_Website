import os
from bson import ObjectId

class LehengaModel:
    def __init__(self, db):
        self.collection = db.lehengas

    def get_all_lehengas(self):
        """Retrieve all lehengas from the database."""
        return [
            {**item, "_id": str(item["_id"])}
            for item in self.collection.find()
        ]

    def get_lehenga_by_id(self, lehenga_id):
        """Retrieve a specific lehenga by its ID."""
        item = self.collection.find_one({"_id": ObjectId(lehenga_id)})
        if item:
            return {**item, "_id": str(item["_id"])}
        return None

    def create_lehenga(self, name, price, image_path):
        """Add a new lehenga to the database."""
        lehenga_data = {
            "name": name,
            "price": price,
            "image": image_path,
        }
        result = self.collection.insert_one(lehenga_data)
        return str(result.inserted_id)

    def update_lehenga(self, lehenga_id, name, price, image_path):
        """Update a specific lehenga by its ID."""
        update_data = {
            "name": name,
            "price": price,
            "image": image_path,
        }
        result = self.collection.update_one(
            {"_id": ObjectId(lehenga_id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_lehenga(self, lehenga_id):
        """Delete a lehenga by its ID."""
        result = self.collection.delete_one({"_id": ObjectId(lehenga_id)})
        return result.deleted_count > 0
