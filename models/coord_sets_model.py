from pymongo.errors import PyMongoError
from bson import ObjectId

class CoordSetModel:
    def __init__(self, db):
        self.collection = db["coord_sets"]

    def create_item(self, name, price, image):
        """
        Create a new coord-set item.
        :param name: Name of the item
        :param price: Price of the item
        :param image: Filename of the image
        :return: Inserted ID or None on failure
        """
        try:
            item = {"name": name, "price": price, "image": image}
            result = self.collection.insert_one(item)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error creating item: {e}")
            return None

    def get_all_items(self):
        """
        Retrieve all coord-set items.
        :return: List of coord-set items or empty list on failure
        """
        try:
            items = self.collection.find()
            return [
                {
                    "_id": str(item["_id"]), 
                    "id": str(item["_id"]),
                    "name": item["name"],
                    "price": item["price"],
                    "image_url": f"{item['image']}"
                }
                for item in items
            ]
        except PyMongoError as e:
            print(f"Error retrieving items: {e}")
            return []

    def get_item_by_id(self, item_id):
        """
        Retrieve a coord-set item by ID.
        :param item_id: ID of the item to fetch
        :return: Item data or None if not found
        """
        try:
            item = self.collection.find_one({"_id": ObjectId(item_id)})
            if item:
                return {
                    "id": str(item["_id"]),
                    "name": item["name"],
                    "price": item["price"],
                    "image_url": f"{item['image']}"
                }
            return None
        except PyMongoError as e:
            print(f"Error retrieving item: {e}")
            return None

    def update_item(self, item_id, update_data):
        """
        Update an existing coord-set item.
        :param item_id: ID of the item to update
        :param update_data: Dictionary of fields to update
        :return: True if updated, False otherwise
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(item_id)}, {"$set": update_data}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating item: {e}")
            return False

    def delete_item(self, item_id):
        """
        Delete a coord-set item.
        :param item_id: ID of the item to delete
        :return: True if deleted, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(item_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting item: {e}")
            return False
