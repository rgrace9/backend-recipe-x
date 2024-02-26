from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import git
import os
from openai import OpenAI
import json
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
from extensions import db
from routes import allergy_bp, ingredient_bp, diet_bp

load_dotenv()

client = OpenAI()

repo = git.Repo.init('.')

app = Flask(__name__)
CORS(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

from models import IngredientCategory, Ingredient, Allergy, Diet, IngredientAllergy, RestrictedDietIngredient

app.register_blueprint(allergy_bp)
app.register_blueprint(ingredient_bp)
app.register_blueprint(diet_bp)

def extract_title_and_description(api_response_str):
    message_data = json.loads(api_response_str)
    
    title = message_data.get("title", "")
    description = message_data.get("description", "")
    
    return {"title": title, "description": description}


def get_chat_message(user_preferences):
    # Construct the system message with instructions
    system_message = {
        "role": "system",
        "content": "You are a recipe creator who returns a single recipe with a title and description that are less than  150 characters for people with allergies, dietary restrictions, and dietary preferences. You follow people's restrictions. All you do is return the name of the one recipe along with description that follow their restrictions. Recipes cannot include vegetable oil or include in the instructions using a non-stick pan, deep frying anything, or frying anything. Get creative with the recipes. Do not keep on returning boring, obvious recipes. You are receiving a JSON of preferences from the user. Any ingredients that are true in the allergies object must absolutely NOT be included in any recipes. There is a dietaryRestrictions object in user JSON input. The dietary restrictions must be followed. The user can select more than one dietaryRestriction. For example, if the user selects kosher and vegan make sure every recipe is vegan and kosher. The recipes must adhere to all of the options. For instance every recipe must not only be kosher but also vegan. Another example is if the user selects both pescatarian and vegan as their dietary restrictions, then every recipe returned must be vegan. Always go with the most restrictive diet. For the specificIngredientsToAvoid value do not return any recipes that include any of the ingredients in the array. For instance, if soy sauce is included in the list do return any recipes that use soy sauce. However you could return recipes that use coconut aminos. Another example is if the user selects both pescatarian and vegan as their dietary restrictions, then every recipe returned must be vegan. Always go with the most restrictive diet. For the specificIngredientsToInclude array only return recipes that include those ingredients. If multiple ingredients are selected not all of them need to be in the recipe. At least one ingredient should be in each recipe. If the specificIngredientsToInclude list contradicts with the user's dietaryRestrictions and allergies, follow the user's dietaryRestrictions and allergies and ignore the contradictory ingredient in the specificIngredientsToInclude array. Include in each recipe at least one item from the randomIngredients array. The meal type options are only: breakfast, lunch, dinner, dessert, snack, beverage. Do not make recipes too similar. We want the user to have a variety of options to choose from. The user might also be submitting a list of recipes they have previously saved. We want the new recipes to be different from the recipes the user has already saved. Do not put oils that are solid at room temperature like coconut oil or butter in a dressing. However, seed and nut butter can be used in dressings if the user is not allergic to them. Return a JSON object code is an array. EXAMPLE RESPONSE. {\"title\": \"Mango & Avocado Sorbet\",\"description\": \" This creamy, dreamy delight blends sweet mangoes and rich avocados for a refreshing, guilt-free indulgence.\"}. Return exactly one recipe. Ingredients to avoid, allergies, and diet preference are very important and must be considered when generating a recipe."
    }

    # Construct the user message with the provided preferences
    user_message = {
        "role": "user",
        "content": user_preferences
    }

    # Create the chat messages array
    messages = [system_message, user_message]

    # Call the OpenAI API to get the chat completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=746,
        top_p=1,
        frequency_penalty=0.03,
        presence_penalty=0
    )

    chat_message = response.choices[0].message.content
    result = extract_title_and_description(chat_message)
    return result


def generate_recipe_ideas_payloads(ingredients_array, user_payload):
    # Randomly select five ingredients
    random_ingredients = random.sample(ingredients_array, 5)
    
    # Prepare payloads for each ingredient
    payloads = []
    for ingredient in random_ingredients:
        payload = user_payload.copy()
        # Set randomIngredients key dynamically
        payload["randomIngredients"] = [ingredient]
        payloads.append(payload)
    
    return payloads

def fetch_random_recipes(user_payloads):
    chat_messages = []
    print('Starting to generate recipes ideas list')
# Iterate through the list of user_payloads
    for user_payload in user_payloads:
        # Generate random ingredients payload for the current user payload

        # Serialize the updated payload to JSON
        data_string = json.dumps(user_payload)

        # Call the method to get the chat message
        chat_message = get_chat_message(data_string)
        # Append the chat message to the list
        chat_messages.append(chat_message)

    # Return the array of chat messages as a JSON response
    print('Finished generating recipes ideas list')

    return chat_messages


def get_acceptable_ingredients(data):
    print('data', data)
    # Query all ingredients
    selected_allergy_ids = data.get('allergyIds', [])
    selected_diet_ids = data.get('dietIds', [])
    ingredients_to_avoid_ids = data.get('excludedIngredientIds', [])

    # Query all ingredients
    ingredients_query = Ingredient.query

    # Exclude ingredients with specified allergy IDs
    if selected_allergy_ids:
        ingredients_query = ingredients_query.filter(~Ingredient.allergies.any(Allergy.id.in_(selected_allergy_ids)))

    # Exclude ingredients with specified diet IDs
    if selected_diet_ids:
        ingredients_query = ingredients_query.filter(~Ingredient.diets.any(Diet.id.in_(selected_diet_ids)))

        # Exclude ingredients to avoid by their IDs
    if ingredients_to_avoid_ids:
        ingredients_query = ingredients_query.filter(~Ingredient.id.in_(ingredients_to_avoid_ids))

    # Fetch the filtered ingredients
    
    filtered_ingredients = ingredients_query.all()

    # Convert the filtered ingredients to a list of dictionaries
    ingredients_list = [ingredient.name for ingredient in filtered_ingredients]

    # Return the filtered ingredients as a JSON response
    return ingredients_list


@app.route('/recipe-ideas', methods=['POST'])
def recipe_ideas():
    user_preferences = request.get_json()
    
    user_ingredients = get_acceptable_ingredients(user_preferences)
    # return
    if 'allergyIds' in user_preferences:
        del user_preferences['allergyIds']
    if 'dietIds' in user_preferences:
        del user_preferences['dietIds']
    if 'excludedIngredientIds' in user_preferences:
        del user_preferences['excludedIngredientIds']
    
    updated_payloads = generate_recipe_ideas_payloads(user_ingredients, user_preferences)
    recipes = fetch_random_recipes(updated_payloads)
    return jsonify(recipes) 

if __name__ == '__main__':
    app.run(debug=True)