from flask import Blueprint, jsonify
from models import Ingredient

ingredient_bp = Blueprint('ingredient_bp', __name__)

@ingredient_bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    # Query the database for all ingredients
    ingredients = Ingredient.query.order_by(Ingredient.name).all()
    # Convert the list of Ingredient objects to a list of dictionaries
    ingredients_list = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredients]
    # Return the data as a JSON response
    return jsonify(ingredients_list)