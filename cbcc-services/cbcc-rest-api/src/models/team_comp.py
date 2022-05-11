from src import db

class TeamComp(db.Model):

    __tablename__ = "team_comp"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_url = db.Column(db.String(80))
    expected_damage = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    phase = db.Column(db.Integer, nullable=False)
    playstyle = db.Column(db.String(80), nullable=False)
    boss_id = db.Column(db.Integer, db.ForeignKey('boss.unit_id'))

    team_comp_characters = db.Relationship('TeamCompCharacter', backref="team_comp")


class TeamCompCharacter(db.Model):

    __tablename__ = "team_comp_character"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    star = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    ue = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    team_comp_id = db.Column(db.Integer, db.ForeignKey('team_comp.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.unit_id'))
