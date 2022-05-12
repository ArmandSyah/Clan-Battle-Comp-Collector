from src import db

class ClanBattle(db.Model):

    __tablename__ = "clan_battle"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clan_battle_id = db.Column(db.Integer, unique=True, nullable=False)
    training_start_date = db.Column(db.DateTime, nullable=False)
    training_end_date = db.Column(db.DateTime, nullable=False)
    main_start_date = db.Column(db.DateTime, nullable=False)
    main_end_date = db.Column(db.DateTime, nullable=False)

    bosses = db.relationship('Boss', backref="clan_battle", cascade="all, delete-orphan")