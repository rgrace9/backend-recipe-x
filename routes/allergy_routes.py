from flask import Blueprint, jsonify
from models import Allergy

allergy_bp = Blueprint('allergy_bp', __name__)


@allergy_bp.route('/allergies', methods=['GET'])
def get_allergies():
    # Query the database for all allergies
    allergies = Allergy.query.order_by(Allergy.name).all()
    
    # Convert the list of Allergy objects to a list of dictionaries
    allergies_list = [{'id': allergy.id, 'name': allergy.name} for allergy in allergies]
    
    # Return the data as a JSON response
    return jsonify(allergies_list)

