from src import db
from flask import request
from flask_restx import Namespace, Resource, fields

from ..models.clan_battle import ClanBattle

clan_battle_namespace = Namespace("cb")

clan_battle = clan_battle_namespace.model(
    "ClanBattle",
    {
        "clan_battle_id": fields.Integer(required=True),
        "training_start_date": fields.DateTime(required=True),
        "training_end_date": fields.DateTime(required=True),
        "main_start_date": fields.DateTime(required=True),
        "main_end_date": fields.DateTime(required=True)
    }
)

class ClanBattleList(Resource):
    @clan_battle_namespace.marshal_with(clan_battle, as_list=True)
    def get(self):
        """Returns all recorded clan battles"""
        return ClanBattle.query.all(), 200
    
    @clan_battle_namespace.expect(clan_battle, validate=True)
    @clan_battle_namespace.response(201, "Clan Battle <clan_battle_id> was added!")
    @clan_battle_namespace.response(400, "Sorry, clan battle already exists")
    def post(self):
        post_data = request.get_json()

        # Parse out fields
        clan_battle_id = post_data.get('clan_battle_id')
        training_start_date = post_data.get('training_start_date')
        training_end_date = post_data.get('training_end_date')
        main_start_date = post_data.get('main_start_date')
        main_end_date = post_data.get('main_end_date')
        response_object = {}

        clan_battle = ClanBattle.query.filter_by(clan_battle_id=clan_battle_id).first()
        if clan_battle:
            response_object["message"] = "Sorry, clan battle already exists"
            return response_object, 400

        clan_battle = ClanBattle(
            clan_battle_id=clan_battle_id,
            training_start_date=training_start_date,
            training_end_date=training_end_date,
            main_start_date=main_start_date,
            main_end_date=main_end_date
        )
        db.session.add(clan_battle)
        db.session.commit()

        response_object["message"] = f'Clan Battle {clan_battle_id} was addded!'
        return response_object, 201

class LatestClanBattle(Resource):
    @clan_battle_namespace.marshal_with(clan_battle)
    def get(self):
        pass

clan_battle_namespace.add_resource(ClanBattleList, "")
clan_battle_namespace.add_resource(LatestClanBattle, "/latest")