from flask import Blueprint, jsonify
from models import Diet

diet_bp = Blueprint('diet_bp', __name__)


@diet_bp.route('/diets', methods=['GET'])
def get_allergies():
    # Query the database for all allergies
    diets = Diet.query.order_by(Diet.name).all()
    
    # Convert the list of diet objects to a list of dictionaries
    diets_list = [{'id': diet.id, 'name': diet.name} for diet in diets]
    
    # Return the data as a JSON response
    return jsonify(diets_list)
