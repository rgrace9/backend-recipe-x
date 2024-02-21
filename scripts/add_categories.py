import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)


from models import IngredientCategory
from app import app 
from extensions import db 

def add_ingredient_categories(category_names):
    with app.app_context():  # Use the app context
        for name in category_names:
            # Convert name to lowercase (or uppercase) to ensure case-insensitivity
            name_lower = name.lower()
            
            # Check if the category already exists in a case-insensitive manner
            existing_category = IngredientCategory.query.filter(IngredientCategory.name.ilike(name_lower)).first()
            if not existing_category:
                # Store the category name in a consistent case format (e.g., lowercase)
                new_category = IngredientCategory(name=name_lower)
                db.session.add(new_category)
                try:
                    db.session.commit()
                    print(f"Added new category: {name_lower}")
                except Exception as e:
                    db.session.rollback()  # Roll back in case of error
                    print(f"Failed to add category {name_lower}. Error: {e}")
            else:
                print(f"Category '{name_lower}' already exists.")

if __name__ == "__main__":
    category_list = ["Vegetables", "Fruits", "Grains", "Dairy", "Proteins", "Fats", "Sweets", "Beverages", "Spices", "Condiments", "Other"]
    add_ingredient_categories(category_list)
