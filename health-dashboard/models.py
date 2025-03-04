from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()
fs = GridFS(db)

class User(UserMixin):
    def __init__(self, username, email, password=None):
        self.id = username
        self.email = email
        if password:
            self.set_password(password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def save(self):
        db.users.insert_one({
            '_id': self.id,
            'email': self.email,
            'password_hash': self.password_hash
        })
    
    @staticmethod
    def get(user_id):
        user_data = db.users.find_one({'_id': user_id})
        if not user_data:
            return None
        user = User(user_data['_id'], user_data['email'])
        user.password_hash = user_data['password_hash']
        return user
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)