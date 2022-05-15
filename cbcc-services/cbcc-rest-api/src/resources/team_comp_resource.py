from tokenize import String

from attr import validate
from src import db
from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import joinedload 

from ..models.team_comp import TeamComp, TeamCompCharacter

team_comp_namespace = Namespace("teamcomp")

character = team_comp_namespace.model(
    "Character",
    {
        "unit_name_en": fields.String(required=True),
        "thematic_en": fields.String,
        "range": fields.Integer,
        "icon": fields.String(required=True)
    }
)

team_comp_character = team_comp_namespace.model(
    "TeamComp_Character",
    {
        "id": fields.Integer(readOnly=True),
        "star": fields.Integer(required=True),
        "rank": fields.Integer(required=True),
        "ue": fields.Integer,
        "level": fields.Integer,
        "notes": fields.String,
        "team_comp_id": fields.Integer,
        "character_id": fields.Integer,
        "character": fields.Nested(character)
    }
)

team_comp = team_comp_namespace.model(
    "TeamComp",
    {
        "id": fields.Integer(readOnly=True),
        "video_url": fields.String,
        "expected_damage": fields.Integer(required=True),
        "notes": fields.String,
        "phase": fields.Integer(required=True),
        "playstyle": fields.String,
        "boss_id": fields.Integer,
        "team_comp_characters": fields.List(fields.Nested(team_comp_character))
    }
)

class TeamComposition(Resource):
    @team_comp_namespace.expect(team_comp, validate=True)
    def post(self):
        "add new team comp"
        post_data = request.get_json()

        # Parse out fields
        video_url = post_data.get('video_url')
        expected_damage = post_data.get('expected_damage')
        notes = post_data.get('notes')
        phase = post_data.get('phase')
        playstyle = post_data.get('playstyle')
        boss_id = post_data.get('boss_id')
        teamcomp_characters = post_data.get('teamcomp_characters')

        response_object = {}

        used_characters = []
        for character in teamcomp_characters:
            new_char = TeamCompCharacter(
                star=character['star'],
                rank=character['rank'],
                ue=character['ue'],
                notes=character['notes'],
                character_id=character['character_id']
            )
            used_characters.append(new_char)

        new_team_comp = TeamComp(
            video_url=video_url,
            expected_damage=expected_damage,
            notes=notes,
            phase=phase,
            playstyle=playstyle,
            boss_id=boss_id,
            team_comp_characters=used_characters
        )

        db.session.add_all(used_characters)
        db.session.add(new_team_comp)
        db.session.commit()

        response_object["message"] = f'Team comp for boss {boss_id} has been added'
        return response_object, 201


class SingleTeamComp(Resource):
    @team_comp_namespace.marshal_with(team_comp)
    def get(self, team_comp_id):
        team_comp = TeamComp.query.options(joinedload(TeamComp.team_comp_characters)).filter(TeamComp.id == team_comp_id).first()
        
        return team_comp, 200
        

team_comp_namespace.add_resource(TeamComposition, "")
team_comp_namespace.add_resource(SingleTeamComp, "/<int:team_comp_id>")