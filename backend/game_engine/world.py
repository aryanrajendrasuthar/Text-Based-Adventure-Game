"""World class — owns and manages all game objects."""
import copy
from typing import Optional
from .models import Room, Item, NPC, Enemy, Player
from .world_data import ROOMS_DATA, ITEMS_DATA, NPCS_DATA, ENEMIES_DATA, ACHIEVEMENTS_DATA


class World:
    def __init__(self):
        self.rooms: dict[str, Room] = {}
        self.items: dict[str, Item] = {}
        self.npcs: dict[str, NPC] = {}
        self.enemies: dict[str, Enemy] = {}
        self.achievements: list[dict] = []
        self._build()

    def _build(self):
        for rid, data in ROOMS_DATA.items():
            self.rooms[rid] = Room(**data)
        for iid, data in ITEMS_DATA.items():
            self.items[iid] = Item(**data)
        for nid, data in NPCS_DATA.items():
            self.npcs[nid] = NPC(**data)
        for eid, data in ENEMIES_DATA.items():
            self.enemies[eid] = Enemy(**data)
        self.achievements = copy.deepcopy(ACHIEVEMENTS_DATA)

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)

    def get_item(self, item_id: str) -> Optional[Item]:
        return self.items.get(item_id)

    def get_npc(self, npc_id: str) -> Optional[NPC]:
        return self.npcs.get(npc_id)

    def get_enemy(self, enemy_id: str) -> Optional[Enemy]:
        return self.enemies.get(enemy_id)

    def get_achievement(self, ach_id: str) -> Optional[dict]:
        for a in self.achievements:
            if a["id"] == ach_id:
                return a
        return None

    def unlock_achievement(self, ach_id: str) -> Optional[str]:
        """Unlock an achievement. Returns its name if newly unlocked, else None."""
        for a in self.achievements:
            if a["id"] == ach_id and not a["unlocked"]:
                a["unlocked"] = True
                self._check_completionist()
                return a["name"]
        return None

    def _check_completionist(self):
        other_ids = {a["id"] for a in self.achievements if a["id"] != "completionist"}
        if all(a["unlocked"] for a in self.achievements if a["id"] in other_ids):
            for a in self.achievements:
                if a["id"] == "completionist":
                    a["unlocked"] = True

    def to_dict(self) -> dict:
        return {
            "rooms": {k: v.to_dict() for k, v in self.rooms.items()},
            "items": {k: v.to_dict() for k, v in self.items.items()},
            "npcs": {k: v.to_dict() for k, v in self.npcs.items()},
            "enemies": {k: v.to_dict() for k, v in self.enemies.items()},
            "achievements": self.achievements,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "World":
        w = cls.__new__(cls)
        w.rooms = {k: Room.from_dict(v) for k, v in data["rooms"].items()}
        w.items = {k: Item.from_dict(v) for k, v in data["items"].items()}
        w.npcs = {k: NPC.from_dict(v) for k, v in data["npcs"].items()}
        w.enemies = {k: Enemy.from_dict(v) for k, v in data["enemies"].items()}
        w.achievements = data["achievements"]
        return w
