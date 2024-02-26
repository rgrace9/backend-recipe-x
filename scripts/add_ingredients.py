import sys
import os
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from models import IngredientAllergy, RestrictedDietIngredient, Ingredient, Allergy, IngredientCategory, Diet
from app import app, client
from extensions import db
from constants import ingredients_list, ingredient_system_content

testing = [
    "Milk",
    "Buttermilk",
    "Heavy cream"
]
def fetch_ingredient_details(ingredient_name):
    print(f"Fetching details for {ingredient_name} with OpenAI")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": ingredient_system_content
            },
            {
                "role": "user",
                "content": ingredient_name
            }
        ],
        temperature=0.3,
        max_tokens=214,
        top_p=0.3,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
    # Assuming the last message in 'choices' contains the ingredient details
        details = response.choices[0].message.content
        print('message', response.choices[0].message)
        ingredient_details = json.loads(details)
        print(f"Successfully fetched details for {ingredient_name}: {ingredient_details}")
        return ingredient_details
    except Exception as e:
        print(f"Error processing ingredient {ingredient_name}: {e}")
        return None


def add_ingredient_with_details(ingredient_data):
    """
    Adds an ingredient to the database with associations to category, diets, and allergies by their IDs.
    Validates the presence of mandatory keys in the ingredient_data dictionary before proceeding.

    :param ingredient_data: Dictionary containing details of the ingredient, including
                            'name', 'category_id', 'restricted_diet_ids', and 'allergy_ids'.
    """
    # Validate expected keys in ingredient_data
    expected_keys = ['name', 'category_id', 'restricted_diet_ids', 'allergy_ids']
    missing_keys = [key for key in expected_keys if key not in ingredient_data]
    if missing_keys:
        print(f"Missing expected keys: {', '.join(missing_keys)}")
        return

    # Extracting values with default for optional keys
    name = ingredient_data['name']
    category_id = ingredient_data['category_id']
    diet_ids = ingredient_data.get('restricted_diet_ids', [])
    allergy_ids = ingredient_data.get('allergy_ids', [])

    existing_ingredient = Ingredient.query.filter(Ingredient.name.ilike(name)).first()

    if existing_ingredient:
        print(f"Ingredient '{name}' already exists. Updating details.")
        if category_id:
            existing_ingredient.category_id = category_id

        try:
            # Handling diets
            RestrictedDietIngredient.query.filter_by(ingredient_id=existing_ingredient.id).delete()
            for diet_id in diet_ids:
                if not db.session.get(Diet, diet_id):
                    print(f"Diet ID '{diet_id}' does not exist. Skipping.")
                    continue
                new_diet_association = RestrictedDietIngredient(ingredient_id=existing_ingredient.id, diet_id=diet_id)
                db.session.add(new_diet_association)

            # Handling allergies
            IngredientAllergy.query.filter_by(ingredient_id=existing_ingredient.id).delete()
            for allergy_id in allergy_ids:
                if not db.session.get(Allergy, allergy_id):
                    print(f"Allergy ID '{allergy_id}' does not exist. Skipping.")
                    continue
                new_allergy_association = IngredientAllergy(ingredient_id=existing_ingredient.id, allergy_id=allergy_id)
                db.session.add(new_allergy_association)

            db.session.commit()
            print(f"Updated '{name}' with new details.")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to update ingredient '{name}'. Error: {e}")
    else:
        if not db.session.query(db.exists().where(IngredientCategory.id == category_id)).scalar():
            print(f"Category with ID '{category_id}' does not exist.")
            return

        new_ingredient = Ingredient(name=name, category_id=category_id)
        db.session.add(new_ingredient)

        try:
            db.session.commit()
            ingredient_id = new_ingredient.id
            # After the ingredient is successfully added, associate it with diets and allergies
            for diet_id in diet_ids:
                if not db.session.get(Diet, diet_id):
                    print(f"Diet ID '{diet_id}' does not exist. Skipping.")
                    continue
                db.session.add(RestrictedDietIngredient(ingredient_id=ingredient_id, diet_id=diet_id))

            for allergy_id in allergy_ids:
                if not db.session.get(Allergy, allergy_id):
                    print(f"Allergy ID '{allergy_id}' does not exist. Skipping.")
                    continue
                db.session.add(IngredientAllergy(ingredient_id=ingredient_id, allergy_id=allergy_id))

            db.session.commit()
            print(f"Added new ingredient '{name}' with details.")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add new ingredient '{name}'. Error: {e}")
    
if __name__ == "__main__":
    for ingredient_name in ingredients_list:
        print(f"Testing that ingredient name {ingredient_name} works.")
        ingredient_details = fetch_ingredient_details(ingredient_name)
        print(f"What OpenAI returned {ingredient_name}: {ingredient_details}")

        with app.app_context():
        # Check if ingredient_details is not None before proceeding
            if ingredient_details:
                add_ingredient_with_details(ingredient_details)
            else:
                print(f"Skipping addition of {ingredient_name} due to an error in processing.")
    # print(f"Testing system messsage {ingredient_system_content} works.")