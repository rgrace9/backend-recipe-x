import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from models import Diet
from app import app
from extensions import db

def add_diets(diet_names):
    with app.app_context():  # Work within the Flask app context
        for name in diet_names:
            name_lower = name.lower()  # Standardize the case
            existing_diet = Diet.query.filter(Diet.name.ilike(name_lower)).first()
            if not existing_diet:
                new_diet = Diet(name=name_lower)
                db.session.add(new_diet)
                try:
                    db.session.commit()
                    print(f"Added new diet: {name_lower}")
                except Exception as e:
                    db.session.rollback()
                    print(f"Failed to add diet {name_lower}. Error: {e}")
            else:
                print(f"Diet '{name_lower}' already exists.")

if __name__ == "__main__":
    diet_list = [
    "Vegan",
    "Vegetarian",
    "Paleo",
    "Ketogenic",
    "Gluten-Free",
    "Low-Carb",
    "Low-Fat",
    "Mediterranean",
    "Pescatarian",
    "Dairy-Free",
    "Whole30",
    "Kosher",
    "Halal",
    "Autoimmune Protocol (AIP)",
    "Raw Food"
]

    add_diets(diet_list)
