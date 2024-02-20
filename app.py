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

load_dotenv()

client = OpenAI()

repo = git.Repo.init('.')

app = Flask(__name__)
CORS(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class IngredientCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    ingredients = db.relationship('Ingredient', backref='category', lazy=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('ingredient_category.id'), nullable=False)

class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Diet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class IngredientAllergy(db.Model):
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.id'), primary_key=True)

class IngredientDiet(db.Model):
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diet.id'), primary_key=True)


# with app.app_context():
    # print("Creating tables")
    # print(os.environ.get('DATABASE_URI'))
    # db.create_all()
    # print("Tables created")
    
# @app.cli.command("reset-db")
# def reset_database():
#     meta = db.metadata
#     for table in reversed(meta.sorted_tables):
#         db.session.execute(text(f"DROP TABLE IF EXISTS {table.name} CASCADE"))
#     db.session.commit()
#     db.create_all()
#     db.session.commit()

class Quotes(Resource):
    def get(self):
        return {
            'Beatles': {
        'quote': ["All you need is love.",
                  "Let it be."]
    }
}

def extract_title_and_description(api_response_str):
    message_data = json.loads(api_response_str)
    
    title = message_data.get("title", "")
    description = message_data.get("description", "")
    
    return {"title": title, "description": description}


def get_chat_message(user_preferences):
    # Construct the system message with instructions
    system_message = {
        "role": "system",
        "content": "You are a recipe creator who returns a single recipe with a title and description that are less than  150 characters for people with allergies, dietary restrictions, and dietary preferences. You follow people's restrictions. All you do is return the name of the one recipe along with description that follow their restrictions. Recipes cannot include vegetable oil or include in the instructions using a non-stick pan, deep frying anything, or frying anything. Get creative with the recipes. Do not keep on returning boring, obvious recipes. You are receiving a JSON of preferences from the user. Any ingredients that are true in the allergies object must absolutely NOT be included in any recipes. There is a dietaryRestrictions object in user JSON input. The dietary restrictions must be followed. The user can select more than one dietaryRestriction. For example, if the user selects kosher and vegan make sure every recipe is vegan and kosher. The recipes must adhere to all of the options. For instance every recipe must not only be kosher but also vegan. Another example is if the user selects both pescatarian and vegan as their dietary restrictions, then every recipe returned must be vegan. Always go with the most restrictive diet. For the specificIngredientsToAvoid value do not return any recipes that include any of the ingredients in the array. For instance, if soy sauce is included in the list do return any recipes that use soy sauce. However you could return recipes that use coconut aminos. Another example is if the user selects both pescatarian and vegan as their dietary restrictions, then every recipe returned must be vegan. Always go with the most restrictive diet. For the specificIngredientsToInclude array only return recipes that include those ingredients. If multiple ingredients are selected not all of them need to be in the recipe. At least one ingredient should be in each recipe. If the specificIngredientsToInclude list contradicts with the user's dietaryRestrictions and allergies, follow the user's dietaryRestrictions and allergies and ignore the contradictory ingredient in the specificIngredientsToInclude array. Include in each recipe at least one item from the randomIngredients array. The meal type options are only: breakfast, lunch, dinner, dessert, snack, beverage. Do not make recipes too similar. We want the user to have a variety of options to choose from. The user might also be submitting a list of recipes they have previously saved. We want the new recipes to be different from the recipes the user has already saved. Do not put oils that are solid at room temperature like coconut oil or butter in a dressing. However, seed and nut butter can be used in dressings if the user is not allergic to them. Return a JSON object code is an array. EXAMPLE RESPONSE. {\"title\": \"Mango & Avocado Sorbet\",\"description\": \" This creamy, dreamy delight blends sweet mangoes and rich avocados for a refreshing, guilt-free indulgence.\"}. Return exactly one recipe"
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


def generate_random_ingredients_payload(ingredients_array, user_payload):
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


@app.route('/recipe-ideas', methods=['POST'])
def recipe_ideas():
    user_preferences = request.get_json()
 
    # generate_random_ingredients_payload(user_preferences["specificIngredientsToInclude"], user_preferences)
    # return
    data_string = json.dumps(user_preferences)


    chat_message = get_chat_message(data_string)

    return jsonify(chat_message)


api.add_resource(Quotes, '/')

if __name__ == '__main__':
    app.run(debug=True)