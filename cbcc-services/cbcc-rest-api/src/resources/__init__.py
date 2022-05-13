from flask_restx import Api

from src.resources.clan_battle_resource import clan_battle_namespace
from src.resources.character_resource import characters_namespace
from src.resources.boss_resource import boss_namespace
from src.resources.ping import ping_namespace
from src.resources.team_comp_resource import team_comp_namespace


api = Api(version="1.0", title="Tsumugi API")

api.add_namespace(clan_battle_namespace, path="/clanbattle")
api.add_namespace(characters_namespace, path="/characters")
api.add_namespace(boss_namespace, path="/bosses")
api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(team_comp_namespace, path="/teamcomp")