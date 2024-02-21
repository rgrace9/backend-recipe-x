from extensions import db

class RestrictedDietIngredient(db.Model):
    __tablename__ = 'restricted_diet_ingredient'
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diet.id'), primary_key=True)
