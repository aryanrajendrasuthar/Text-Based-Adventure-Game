from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import random


@dataclass
class Item:
    id: str
    name: str
    description: str
    item_type: str  # weapon, armor, consumable, key, quest
    value: int = 0
    effect: int = 0  # HP restore for consumables, attack bonus for weapons, defense bonus for armor
    quantity: int = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "item_type": self.item_type,
            "value": self.value,
            "effect": self.effect,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(**data)


@dataclass
class NPC:
    id: str
    name: str
    description: str
    dialogue_tree: dict  # {"default": "...", "after_quest": "...", etc.}
    current_state: str = "default"
    gives_item: Optional[str] = None  # item id
    item_given: bool = False
    quest_complete: bool = False

    def get_dialogue(self) -> str:
        return self.dialogue_tree.get(self.current_state, self.dialogue_tree.get("default", "..."))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "dialogue_tree": self.dialogue_tree,
            "current_state": self.current_state,
            "gives_item": self.gives_item,
            "item_given": self.item_given,
            "quest_complete": self.quest_complete,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NPC":
        return cls(**data)


@dataclass
class Enemy:
    id: str
    name: str
    description: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    xp_reward: int
    gold_reward: int
    is_boss: bool = False
    drops: list[str] = field(default_factory=list)  # item ids
    ascii_art: str = ""
    defeated: bool = False

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> int:
        actual = max(1, damage)
        self.hp = max(0, self.hp - actual)
        return actual

    def attack_player(self, player_defense: int) -> int:
        raw = self.attack - player_defense + random.randint(1, 6)
        return max(1, raw)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "is_boss": self.is_boss,
            "drops": self.drops,
            "ascii_art": self.ascii_art,
            "defeated": self.defeated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Enemy":
        return cls(**data)


@dataclass
class Room:
    id: str
    name: str
    description: str
    ascii_art: str
    exits: dict[str, str]  # {"north": "room_id", ...}
    items: list[str] = field(default_factory=list)  # item ids present in room
    npcs: list[str] = field(default_factory=list)   # npc ids present in room
    enemies: list[str] = field(default_factory=list)  # enemy ids present in room
    visited: bool = False
    locked: bool = False
    lock_key: Optional[str] = None  # item id needed to unlock
    special_action: Optional[str] = None  # triggers a special event

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ascii_art": self.ascii_art,
            "exits": self.exits,
            "items": self.items,
            "npcs": self.npcs,
            "enemies": self.enemies,
            "visited": self.visited,
            "locked": self.locked,
            "lock_key": self.lock_key,
            "special_action": self.special_action,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Room":
        return cls(**data)


@dataclass
class Player:
    name: str
    hp: int = 100
    max_hp: int = 100
    attack: int = 10
    defense: int = 5
    inventory: list[str] = field(default_factory=list)  # item ids
    current_room: str = "village_entrance"
    gold: int = 0
    xp: int = 0
    level: int = 1
    equipped_weapon: Optional[str] = None
    equipped_armor: Optional[str] = None
    # track key story flags
    flags: dict = field(default_factory=dict)

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> int:
        actual = max(1, damage)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount: int) -> int:
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def gain_xp(self, amount: int) -> bool:
        """Returns True if leveled up."""
        self.xp += amount
        level_threshold = self.level * 50
        if self.xp >= level_threshold:
            self.level += 1
            self.max_hp += 20
            self.hp = min(self.hp + 20, self.max_hp)
            self.attack += 3
            self.defense += 2
            return True
        return False

    def get_attack_power(self) -> int:
        return self.attack

    def get_defense_power(self) -> int:
        return self.defense

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "inventory": self.inventory,
            "current_room": self.current_room,
            "gold": self.gold,
            "xp": self.xp,
            "level": self.level,
            "equipped_weapon": self.equipped_weapon,
            "equipped_armor": self.equipped_armor,
            "flags": self.flags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(**data)
