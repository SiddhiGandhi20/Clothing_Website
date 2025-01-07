from flask import request
from pymongo.errors import PyMongoError
from bson import ObjectId

class KurtaSetDetailModel:
    def __init__(self, db):
        self.collection = db["kurtaset_details"]

    def create_item(self, name, description, image, price, kurtaset_id):
        """
        Create a new kurtaset_details item.
        :param name: Name of the item
        :param description: Description of the item
        :param image: Filename of the image
        :param price: Price of the item
        :param kurtaset_id: ID of the associated blazer set
        :return: Inserted ID or None on failure
        """
        try:
            item = {
                "name": name,
                "description": description,
                "image": image,
                "price": price,
                "kurtaset_id": ObjectId(kurtaset_id),
            }
            result = self.collection.insert_one(item)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error creating item: {e}")
            return None

    def get_all_items(self):
        """
        Retrieve all kurtaset_details items.
        :return: List of kurtaset_details items or empty list on failure
        """
        try:
            items = self.collection.find()
            return [
                {
                    "id": str(item["_id"]),
                    "name": item["name"],
                    "description": item["description"],
                    "image_url": f"{request.host_url}{item['image']}",  # Fix path here
                    "price": item["price"],
                    "kurtaset_id": str(item["kurtaset_id"]),
                }
                for item in items
            ]
        except PyMongoError as e:
            print(f"Error retrieving items: {e}")
            return []

    # get_item_by_id method
    # Update method signature to accept base_url
    def get_item_by_id(self, item_id, base_url=None):
        """
        Retrieve a kurtaset_details item by ID.
        :param item_id: ID of the item to fetch
        :param base_url: Optional base URL to format image URL (default: None)
        :return: Item data or None if not found
        """
        try:
            item = self.collection.find_one({"_id": ObjectId(item_id)})
            if item:
                # If base_url is provided, use it, otherwise use request.host_url
                image_url = f"{base_url or request.host_url}{item['image']}"
                return {
                    "id": str(item["_id"]),
                    "name": item["name"],
                    "description": item["description"],
                    "image_url": image_url,  # Fix path here
                    "price": item["price"],
                    "kurtaset_id": str(item["kurtaset_id"]),
                }
            return None
        except PyMongoError as e:
            print(f"Error retrieving item: {e}")
            return None


    def update_item(self, item_id, update_data):
        """
        Update an existing kurtaset_details item.
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
        Delete a kurtaset_details item.
        :param item_id: ID of the item to delete
        :return: True if deleted, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(item_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting item: {e}")
            return False
