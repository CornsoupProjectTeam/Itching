from app import mongo

class ChatRoomRepository:
    @staticmethod
    def insert_chat_room(chat_room_data):
        chat_room_collection = mongo.db.chat_rooms
        chat_room_collection.insert_one(chat_room_data)

    @staticmethod
    def get_all_chat_rooms():
        chat_room_collection = mongo.db.chat_rooms
        return chat_room_collection.find()


