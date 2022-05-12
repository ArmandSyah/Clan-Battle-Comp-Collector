from src import db

class Character(db.Model):
    
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.Integer, unique=True, nullable=False)
    unit_name = db.Column(db.String(80), nullable=False)
    unit_name_en = db.Column(db.String(80), nullable=False)
    thematic = db.Column(db.String(80))
    thematic_en = db.Column(db.String(80))
    range = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.String(200), unique=True, nullable=False)
    max_star = db.Column(db.Integer, nullable=False)

    team_comp_characters = db.relationship('TeamCompCharacter', backref="character", cascade="all, delete-orphan")