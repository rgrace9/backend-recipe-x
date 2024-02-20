from extensions import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('ingredient_category.id'), nullable=False)