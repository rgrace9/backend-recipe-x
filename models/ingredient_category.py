from extensions import db

class IngredientCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    ingredients = db.relationship('Ingredient', backref='category', lazy=True)