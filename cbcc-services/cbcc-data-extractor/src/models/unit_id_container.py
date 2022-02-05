class UnitIdContainer():
    def __init__(self, unit_id, playable_character = False) -> None:
        self.unit_id = unit_id
        self.playable_character = playable_character
        self.one_star_icon_id = f'{unit_id[0:4]}1{unit_id[5]}' if playable_character else None
        self.three_star_icon_id = f'{unit_id[0:4]}3{unit_id[5]}' if playable_character else None
        self.six_star_icon_id = f'{unit_id[0:4]}6{unit_id[5]}' if playable_character else None
        
    def get_icon_ids(self):
        return [self.one_star_icon_id, self.three_star_icon_id, self.six_star_icon_id] if self.playable_character else [self.unit_id]