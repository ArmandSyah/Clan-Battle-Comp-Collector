from src import db
from flask import request
from flask_restx import Namespace, Resource, fields

from ..models.character import Character

characters_namespace = Namespace("characters")

character = characters_namespace.model(
    "Character",
    {
        "id": fields.Integer(readOnly=True),
        "unit_id": fields.Integer(required=True),
        "unit_name": fields.String(required=True),
        "unit_name_en": fields.String(required=True),
        "thematic": fields.String,
        "thematic_en": fields.String,
        "range": fields.Integer,
        "icon": fields.String(required=True),
        "max_star": fields.Integer
    }
)

class CharacterList(Resource):
    @characters_namespace.marshal_with(character, as_list=True)
    def get(self):
        """Gets all the characters"""
        return Character.query.all(), 200

    @characters_namespace.expect(character, validate=True)
    @characters_namespace.response(201, "Clan Battle <clan_battle_id> was added!")
    @characters_namespace.response(400, "Sorry, character already exists")
    def post(self):
        """Add in a new character"""
        post_data = request.get_json()

        # Parse out fields
        unit_id = post_data.get('unit_id')
        unit_name = post_data.get('unit_name')
        unit_name_en = post_data.get('unit_name_en')
        thematic = post_data.get('thematic')
        thematic_en = post_data.get('thematic_en')
        range = post_data.get('range')
        icon = post_data.get('icon')
        max_star = post_data.get('max_star')

        response_object = {}

        character = Character.query.filter_by(unit_id=unit_id).first()
        if character:
            response_object["message"] = "Sorry, character already exists"
            return response_object, 400

        character = Character(
            unit_id = unit_id,
            unit_name = unit_name,
            unit_name_en = unit_name_en,
            thematic = thematic,
            thematic_en = thematic_en,
            range = range,
            icon = icon,
            max_star = max_star
        )
        db.session.add(character)
        db.session.commit()

        response_object["message"] = f'Character {unit_name_en} was addded!'
        return response_object, 201

class SingleCharacter(Resource):
    @characters_namespace.expect(character, validate=True)
    @characters_namespace.response(200, "Character <character_id> was updated!")
    @characters_namespace.response(404, "Character with ID <character_id> does not exist")
    def put(self, unit_id):
        """updates a character"""
        post_data = request.get_json()

        # parse out fields
        max_star = post_data.get('max_star')

        response_object = {}

        character = Character.query.filter_by(unit_id=unit_id).first()
        if not character:
            characters_namespace.abort(404, f"Character with ID {unit_id} does not exist")

        character.max_star = max_star
        db.session.commit()

        response_object["message"] = f"Character {character.unit_id} was updated!"
        return response_object, 200

characters_namespace.add_resource(CharacterList, "")
characters_namespace.add_resource(SingleCharacter, "/<int:unit_id>")