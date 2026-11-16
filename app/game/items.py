"""Gear catalog. Gear is cosmetic only: it never changes who wins.

Ids match art/blender/make_sprites.py and the image names in art/renders.
An item is either unlocked by reaching a rank or bought with coins.
"""

ITEMS = (
    {"id": "gold-armor", "fighter": "knight", "name": "Gold Armor", "color": "#e8b04a", "unlock_rank": 1, "price": None},
    {"id": "flame-bow", "fighter": "archer", "name": "Flame Bow", "color": "#ff7a3d", "unlock_rank": 2, "price": None},
    {"id": "storm-staff", "fighter": "wizard", "name": "Storm Staff", "color": "#4fc3f7", "unlock_rank": 3, "price": None},
    {"id": "dragon-shield", "fighter": "knight", "name": "Dragon Shield", "color": "#d64545", "unlock_rank": None, "price": 30},
    {"id": "shadow-cloak", "fighter": "archer", "name": "Shadow Cloak", "color": "#8f8fb8", "unlock_rank": None, "price": 30},
    {"id": "arcane-purple", "fighter": "wizard", "name": "Arcane Purple", "color": "#c069ff", "unlock_rank": None, "price": 30},
)

_BY_ID = {item["id"]: item for item in ITEMS}


def get_item(item_id):
    return _BY_ID.get(item_id)


def items_unlocked_at(rank: int):
    """Ids of items awarded for reaching `rank`."""
    return [item["id"] for item in ITEMS if item["unlock_rank"] == rank]
