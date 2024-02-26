from flask import Blueprint, jsonify, request
from models import Ingredient, Diet, Allergy

ingredient_bp = Blueprint('ingredient_bp', __name__)

@ingredient_bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    # Query the database for all ingredients
    ingredients = Ingredient.query.order_by(Ingredient.name).all()
    # Convert the list of Ingredient objects to a list of dictionaries
    ingredients_list = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredients]
    # Return the data as a JSON response
    return jsonify(ingredients_list)

@ingredient_bp.route('/filter-ingredients', methods=['POST'])
def filter_ingredients():
    data = request.json
    selected_allergy_ids = data.get('allergyIds', [])
    selected_diet_ids = data.get('dietIds', [])

    # Query all ingredients
    ingredients_query = Ingredient.query

    # Exclude ingredients with specified allergy IDs
    if selected_allergy_ids:
        ingredients_query = ingredients_query.filter(~Ingredient.allergies.any(Allergy.id.in_(selected_allergy_ids)))

    # Exclude ingredients with specified diet IDs
    if selected_diet_ids:
        ingredients_query = ingredients_query.filter(~Ingredient.diets.any(Diet.id.in_(selected_diet_ids)))

    # Fetch the filtered ingredients
    filtered_ingredients = ingredients_query.all()

    # Convert the filtered ingredients to a list of dictionaries
    ingredients_list = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in filtered_ingredients]

    # Return the filtered ingredients as a JSON response
    return jsonify(ingredients_list)