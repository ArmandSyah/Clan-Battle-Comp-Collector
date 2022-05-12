from flask_sqlalchemy import SQLAlchemy
from src import db

class Boss(db.Model):

    __tablename__ = "boss"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.Integer, nullable=False)
    unit_name = db.Column(db.String(80), nullable=False)
    unit_name_en = db.Column(db.String(80), nullable=False)
    icon = db.Column(db.String(200), nullable=False)
    clan_battle_id = db.Column(db.Integer, db.ForeignKey('clan_battle.clan_battle_id'))

    team_comps = db.relationship('TeamComp', backref="boss", cascade="all, delete-orphan")