from flask_restx import Api

from src.resources.clan_battle_resource import clan_battle_namespace
from src.resources.character_resource import characters_namespace
from src.resources.boss_resource import boss_namespace

api = Api(version="1.0", title="Tsumugi API")

api.add_namespace(clan_battle_namespace, path="/clanbattle")
api.add_namespace(characters_namespace, path="/characters")
api.add_namespace(boss_namespace, path="/bosses")