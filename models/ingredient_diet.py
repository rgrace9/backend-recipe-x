from extensions import db

class IngredientDiet(db.Model):
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diet.id'), primary_key=True)
