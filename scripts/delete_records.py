import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from models import RestrictedDietIngredient, IngredientAllergy, Ingredient, IngredientCategory
from app import app
from extensions import db


with app.app_context():
    # Attempt to delete records from the tables, respecting foreign key constraints.
    try:
        # First, delete records from the RestrictedDietIngredient table
        db.session.query(RestrictedDietIngredient).delete()
        db.session.query(IngredientAllergy).delete()
        # Commit the changes to ensure the deletions are applied
        db.session.commit()

        # Then, delete records from the Ingredient table
        db.session.query(Ingredient).delete()
        # Commit again

        # Final commit
        db.session.commit()
        print("Tables cleared successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to clear tables: {e}")
