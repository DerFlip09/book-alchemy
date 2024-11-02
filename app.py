from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from data_models import db, Author, Book
import os

app = Flask(__name__)

# Get the absolute path to the current directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Set the database URI to point to the data directory
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "data", "library.sqlite3")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create the tables
# with app.app_context():
#     print("Creating tables...")
#     db.create_all()  # Create all tables based on the defined models
#     print("Tables created.")

@app.route('/')
def index():
    return "Hello, Library!"


if __name__ == '__main__':
    app.run(debug=True)
