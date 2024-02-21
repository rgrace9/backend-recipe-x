import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from models import Allergy
from app import app 
from extensions import db


def add_allergies(allergy_names):
    with app.app_context():  # Work within the Flask app context
        for name in allergy_names:
            name_lower = name.lower()  # Standardize the case
            existing_allergy = Allergy.query.filter(Allergy.name.ilike(name_lower)).first()
            if not existing_allergy:
                new_allergy = Allergy(name=name_lower)
                db.session.add(new_allergy)
                try:
                    db.session.commit()
                    print(f"Added new allergy: {name_lower}")
                except Exception as e:
                    db.session.rollback()
                    print(f"Failed to add allergy {name_lower}. Error: {e}")
            else:
                print(f"Allergy '{name_lower}' already exists.")

if __name__ == "__main__":
    allergy_list = [
    "Peanuts",
    "Tree Nuts",
    "Milk",
    "Eggs",
    "Fish",
    "Shellfish",
    "Wheat",
    "Soy",
    "Sesame",
    "Corn",
    "Mustard",
    "Celery"
]
    add_allergies(allergy_list)
