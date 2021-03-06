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
        "icon": fields.String(required=True),
    },
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
        "character": fields.Nested(character),
    },
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
        "team_comp_characters": fields.List(fields.Nested(team_comp_character)),
    },
)

team_comps = team_comp_namespace.model(
    "TeamComps", {"team_comps": fields.List(fields.Nested(team_comp))}
)


class TeamComposition(Resource):
    @team_comp_namespace.expect(team_comp, validate=True)
    @team_comp_namespace.response(201, "Team comp for boss <id> has been added")
    def post(self):
        "add new team comp"
        post_data = request.get_json()

        # Parse out fields
        video_url = post_data.get("video_url")
        expected_damage = post_data.get("expected_damage")
        notes = post_data.get("notes")
        phase = post_data.get("phase")
        playstyle = post_data.get("playstyle")
        boss_id = post_data.get("boss_id")
        teamcomp_characters = post_data.get("teamcomp_characters")

        response_object = {}

        used_characters = []
        for character in teamcomp_characters:
            new_char = TeamCompCharacter(
                star=character.get("star"),
                rank=character.get("rank"),
                ue=character.get("ue"),
                notes=character.get("notes"),
                character_id=character.get("character_id"),
                level=character.get("level")
            )
            used_characters.append(new_char)

        new_team_comp = TeamComp(
            video_url=video_url,
            expected_damage=expected_damage,
            notes=notes,
            phase=phase,
            playstyle=playstyle,
            boss_id=boss_id,
            team_comp_characters=used_characters,
        )

        db.session.add_all(used_characters)
        db.session.add(new_team_comp)
        db.session.commit()

        response_object["message"] = f"Team comp for boss {boss_id} has been added"
        return response_object, 201


class SingleTeamComp(Resource):
    @team_comp_namespace.marshal_with(team_comp)
    def get(self, team_comp_id):
        team_comp = (
            TeamComp.query.options(joinedload(TeamComp.team_comp_characters))
            .filter(TeamComp.id == team_comp_id)
            .first()
        )

        return team_comp, 200

    @team_comp_namespace.response(200, "Team comp <team_comp_id> was updated!")
    @team_comp_namespace.response(404, "Team comp <team_comp_id> does not exist")
    @team_comp_namespace.expect(team_comp, validate=True)
    def put(self, team_comp_id):
        put_data = request.get_json()

        # Parse out fields
        video_url = put_data.get("video_url")
        expected_damage = put_data.get("expected_damage")
        notes = put_data.get("notes")
        phase = put_data.get("phase")
        playstyle = put_data.get("playstyle")
        teamcomp_characters = put_data.get("teamcomp_characters")

        response_object = {}

        team_comp : TeamComp = TeamComp.query.get(team_comp_id)
        if not team_comp:
            team_comp_namespace.abort(404, f"Team comp {team_comp_id} does not exist")

        # Bulk Delete the team comp characters, and then put in the new ones
        TeamCompCharacter.query.filter_by(team_comp_id=team_comp_id).delete()

        used_characters = []
        for character in teamcomp_characters:
            new_char = TeamCompCharacter(
                star=character.get("star"),
                rank=character.get("rank"),
                ue=character.get("ue"),
                notes=character.get("notes"),
                character_id=character.get("character_id"),
                level=character.get("level")
            )
            used_characters.append(new_char)

        team_comp.video_url = video_url
        team_comp.expected_damage = expected_damage
        team_comp.notes = notes
        team_comp.phase = phase
        team_comp.playstyle = playstyle
        team_comp.team_comp_characters = used_characters

        db.session.add_all(used_characters)
        db.session.commit()

        response_object["message"] = f"Team comp {team_comp_id} was updated!"
        return response_object, 200
    
    @team_comp_namespace.response(200, "Team Comp <team_comp_id> was removed!")
    @team_comp_namespace.response(404, "Team Comp <team_comp_id> does not exist")
    def delete(self, team_comp_id):
        response_object = {}
        team_comp = TeamComp.query.filter(TeamComp.id == team_comp_id).first()

        if not team_comp:
            team_comp_namespace.abort(404, f"Team Comp {team_comp_id} does not exist")
        
        db.session.delete(team_comp)
        db.session.commit()

        response_object["message"] = f'Team Comp {team_comp_id} was removed!'
        return response_object, 200


class MultipleTeamComps(Resource):
    @team_comp_namespace.marshal_with(team_comps)
    @team_comp_namespace.response(201, "Added <team_comps> new team comps")
    def post(self):
        "Add multiple team comps"
        post_data = request.get_json()

        # parse out fields
        team_comps = post_data.get("team_comps")

        response_object = {}

        team_comp_list = []
        for team_comp in team_comps:
            teamcomp_characters = team_comp.get("team_comp_characters")
            used_characters = []
            for character in teamcomp_characters:
                new_char = TeamCompCharacter(
                    star=character.get("star"),
                    rank=character.get("rank"),
                    ue=character.get("ue"),
                    notes=character.get("notes"),
                    character_id=character.get("character_id"),
                )
                used_characters.append(new_char)

            video_url = team_comp.get("video_url")
            expected_damage = team_comp.get("expected_damage")
            notes = team_comp.get("notes")
            phase = team_comp.get("phase")
            playstyle = team_comp.get("playstyle")
            boss_id = team_comp.get("boss_id")

            new_team_comp = TeamComp(
                video_url=video_url,
                expected_damage=expected_damage,
                notes=notes,
                phase=phase,
                playstyle=playstyle,
                boss_id=boss_id,
                team_comp_characters=used_characters,
            )

            db.session.add_all(used_characters)
            team_comp_list.append(new_team_comp)

        db.session.add_all(team_comp_list)
        db.session.commit()

        response_object["message"] = f"Added {len(team_comp_list)} new team comps"
        return response_object, 201


team_comp_namespace.add_resource(TeamComposition, "")
team_comp_namespace.add_resource(SingleTeamComp, "/<int:team_comp_id>")
team_comp_namespace.add_resource(MultipleTeamComps, "/multiple")
