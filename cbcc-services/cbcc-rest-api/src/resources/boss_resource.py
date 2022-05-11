from src import db
from flask import request
from flask_restx import Namespace, Resource, fields

from ..models.boss import Boss
from ..models.clan_battle import ClanBattle

boss_namespace = Namespace("bosses")

boss = boss_namespace.model(
    "Boss",
    {
        "id": fields.Integer(readOnly=True),
        "unit_id": fields.Integer(required=True),
        "unit_name": fields.String(required=True),
        "unit_name_en": fields.String(required=True),
        "icon": fields.String(required=True),
        "clan_battle_id": fields.Integer
    }
)


class BossList(Resource):
    @boss_namespace.expect(boss, validate=True)
    @boss_namespace.response(201, "Boss <boss_name> was added!")
    @boss_namespace.response(400, "Sorry, boss already exists")
    @boss_namespace.response(401, "Clan Battle with ID <clan_battle_id> does not exist")
    def post(self):
        """Create a new boss for the clan battle instance"""
        post_data = request.get_json()

        # Parse out fields
        unit_id = post_data.get('unit_id')
        unit_name = post_data.get('unit_name')
        unit_name_en = post_data.get('unit_name_en')
        icon = post_data.get('icon')
        clan_battle_id = post_data.get('clan_battle_id')

        response_object = {}

        boss = Boss.query.filter_by(unit_id=unit_id).first()
        if boss:
            response_object["message"] = "Sorry, boss already exists"
            return response_object, 400
        
        clan_battle = ClanBattle.query.filter_by(clan_battle_id=clan_battle_id).first()
        if not clan_battle:
            boss_namespace.abort(404, f"Clan Battle with ID {clan_battle_id} does not exist")

        boss = Boss(
            unit_id = unit_id,
            unit_name = unit_name,
            unit_name_en = unit_name_en,
            icon = icon,
            clan_battle_id = clan_battle_id
        )
        db.session.add(boss)
        db.session.commit()

        response_object["message"] = f'Boss {boss.unit_name_en} was addded!'
        return response_object, 201
 
boss_namespace.add_resource(BossList, "")