from extensions import db

class IngredientAllergy(db.Model):
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.id'), primary_key=True)