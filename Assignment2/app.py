from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

import os
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

app = Flask(__name__)

# MongoDB connection setup
client = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_{PASSWORD}@devops.9yjoy.mongodb.net/?retryWrites=true&w=majority&appName=DevOps"
db = client.shop_db
products_collection = db['products']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    products = products_collection.find()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
