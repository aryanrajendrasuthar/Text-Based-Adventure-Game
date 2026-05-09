"""
Static world data for "The Lost Kingdom of Aethermoor".
20 rooms, 3 boss enemies, 5 NPCs, 15 items, 3 endings.
"""

ITEMS_DATA = {
    "rusty_sword": {
        "id": "rusty_sword", "name": "Rusty Sword", "item_type": "weapon",
        "description": "A worn sword found near the village gate. It will do for now.",
        "value": 5, "effect": 3, "quantity": 1,
    },
    "health_potion": {
        "id": "health_potion", "name": "Health Potion", "item_type": "consumable",
        "description": "A vial of red liquid that restores 30 HP when consumed.",
        "value": 10, "effect": 30, "quantity": 1,
    },
    "leather_shield": {
        "id": "leather_shield", "name": "Leather Shield", "item_type": "armor",
        "description": "A cracked leather shield. Provides modest protection (+4 defense).",
        "value": 8, "effect": 4, "quantity": 1,
    },
    "ancient_tome": {
        "id": "ancient_tome", "name": "Ancient Tome", "item_type": "quest",
        "description": "A dusty tome with faded writing. Contains lore about the Dark Sorcerer Malachar.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "torch": {
        "id": "torch", "name": "Torch", "item_type": "key",
        "description": "A lit torch that illuminates dark passages.",
        "value": 2, "effect": 0, "quantity": 1,
    },
    "cave_map": {
        "id": "cave_map", "name": "Cave Map", "item_type": "quest",
        "description": "A hand-drawn map of the underground cave system. Shows a hidden passage.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "crystal_shard": {
        "id": "crystal_shard", "name": "Crystal Shard", "item_type": "quest",
        "description": "A glowing shard of a broken ward crystal. Radiates protective magic.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "rope": {
        "id": "rope", "name": "Sturdy Rope", "item_type": "key",
        "description": "A coiled rope useful for climbing or securing things.",
        "value": 3, "effect": 0, "quantity": 1,
    },
    "guard_key": {
        "id": "guard_key", "name": "Guard's Key", "item_type": "key",
        "description": "An iron key engraved with the royal crest. Opens the castle inner door.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "dungeon_key": {
        "id": "dungeon_key", "name": "Dungeon Key", "item_type": "key",
        "description": "A heavy iron key that unlocks the castle dungeon cells.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "royal_sword": {
        "id": "royal_sword", "name": "Royal Sword", "item_type": "weapon",
        "description": "A gleaming sword bearing the royal family's crest. Strong and well-balanced (+10 attack).",
        "value": 50, "effect": 10, "quantity": 1,
    },
    "dark_orb": {
        "id": "dark_orb", "name": "Dark Orb", "item_type": "quest",
        "description": "A pulsating orb of shadow energy. It whispers promises of power. You feel uneasy holding it.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "purification_stone": {
        "id": "purification_stone", "name": "Purification Stone", "item_type": "quest",
        "description": "A radiant white stone blessed by the Spirit Guardian. Can dispel dark magic.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "enchanted_armor": {
        "id": "enchanted_armor", "name": "Enchanted Armor", "item_type": "armor",
        "description": "Gleaming armor infused with protective runes (+12 defense).",
        "value": 80, "effect": 12, "quantity": 1,
    },
    "ancient_artifact": {
        "id": "ancient_artifact", "name": "Ancient Artifact", "item_type": "quest",
        "description": "The Heartstone of Aethermoor — the source of the kingdom's life force. Its glow fills you with warmth.",
        "value": 0, "effect": 0, "quantity": 1,
    },
    "elixir_of_strength": {
        "id": "elixir_of_strength", "name": "Elixir of Strength", "item_type": "consumable",
        "description": "A shimmering blue elixir that permanently increases attack by 5.",
        "value": 30, "effect": 5, "quantity": 1,
    },
    "greater_health_potion": {
        "id": "greater_health_potion", "name": "Greater Health Potion", "item_type": "consumable",
        "description": "A large flask of healing liquid. Restores 60 HP.",
        "value": 25, "effect": 60, "quantity": 1,
    },
}

NPCS_DATA = {
    "innkeeper_bertha": {
        "id": "innkeeper_bertha",
        "name": "Bertha the Innkeeper",
        "description": "A stout woman with kind eyes and flour on her apron.",
        "dialogue_tree": {
            "default": (
                "Bertha looks up from wiping the counter.\n"
                "'Welcome, traveller. These are dark times for Aethermoor. The sorcerer Malachar "
                "seized the castle a fortnight ago. The king is missing — some say imprisoned.\n"
                "If you seek to help, speak with old Wizard Alara at the library. She knows more "
                "of Malachar's weakness. And be careful in the forest — his corrupted beasts roam freely now.'"
            ),
            "has_tome": (
                "'You found the tome! Alara will be able to translate it. She's in the old library "
                "to the east of the village square. Hurry, brave one — every day Malachar grows stronger.'"
            ),
            "after_spirit": (
                "'The Spirit Guardian blessed you? Then there is hope yet! Go face Malachar. "
                "Aethermoor depends on you.'"
            ),
        },
        "gives_item": None,
        "item_given": False,
        "quest_complete": False,
        "current_state": "default",
    },
    "blacksmith_garrett": {
        "id": "blacksmith_garrett",
        "name": "Garrett the Blacksmith",
        "description": "A broad-shouldered man with a bushy beard and soot-covered hands.",
        "dialogue_tree": {
            "default": (
                "Garrett doesn't look up from his work.\n"
                "'Shop's closed. No point making weapons when Malachar's minions will just take them.'\n"
                "He pauses, then sighs. 'Fine, look around. Take the shield — I've no use for it. "
                "Just... bring back proof the tyrant is dead, will you?'"
            ),
            "after_boss1": (
                "'You defeated the Guard Captain?! Ha! There's hope for this kingdom yet. "
                "I forged that Royal Sword for the king himself — use it well.'"
            ),
        },
        "gives_item": "leather_shield",
        "item_given": False,
        "quest_complete": False,
        "current_state": "default",
    },
    "wizard_alara": {
        "id": "wizard_alara",
        "name": "Alara the Wizard",
        "description": "An elderly woman surrounded by floating candles, her silver hair tied back with a ribbon.",
        "dialogue_tree": {
            "default": (
                "Alara peers over her spectacles.\n"
                "'Ah, a hero arrives at last. Malachar was once my student — brilliant, but consumed "
                "by ambition. He seeks the Ancient Artifact, the Heartstone of Aethermoor, buried "
                "in his sanctum at the top of the Dark Tower.\n"
                "You must reach it before he can use it. To defeat him, you will need the Purification Stone "
                "— seek the Spirit Guardian in the Crystal Chamber beneath the cave system.\n"
                "But be warned: the path is treacherous. Bring the Ancient Tome if you find it — "
                "it holds the binding words that will activate the stone.'"
            ),
            "has_tome": (
                "Alara's eyes light up as you hand her the tome.\n"
                "'Yes! This is exactly what I needed. The binding incantation... listen carefully.\n"
                "When you use the Purification Stone on Malachar, speak these words: "
                "'By light of truth and will unbound, let darkness fail and hope be found.'\n"
                "Go now — and may the old magic guide you.'"
            ),
        },
        "gives_item": None,
        "item_given": False,
        "quest_complete": False,
        "current_state": "default",
    },
    "prisoner_theron": {
        "id": "prisoner_theron",
        "name": "Theron the Prisoner",
        "description": "A gaunt man chained to the dungeon wall, eyes wild with desperation.",
        "dialogue_tree": {
            "default": (
                "Theron rattles his chains.\n"
                "'Please, get me out of here! I was the castle's head steward before Malachar came. "
                "I know the secret passage to the tower — release me and I'll show you!'\n"
                "(You need the Dungeon Key to free him.)"
            ),
            "freed": (
                "Theron rubs his wrists gratefully.\n"
                "'Thank you. Listen — behind the throne there is a hidden lever. Pull it and a "
                "passage opens to the Dark Tower staircase. Malachar uses it to avoid the main halls.\n"
                "Also... in the Secret Chamber off the dungeon, I saw him store a Dark Orb. "
                "Do not touch it — it is a focus of his corruption. Destroy it if you can.'"
            ),
        },
        "gives_item": None,
        "item_given": False,
        "quest_complete": False,
        "current_state": "default",
    },
    "spirit_guardian": {
        "id": "spirit_guardian",
        "name": "The Spirit Guardian",
        "description": "A translucent figure of pure light shaped like an ancient warrior.",
        "dialogue_tree": {
            "default": (
                "The spirit's voice resonates like a distant bell.\n"
                "'Mortal... you seek to challenge the darkness that grips this realm. "
                "Know this: Malachar's power stems from the Heartstone he corrupted. "
                "Only the Purification Stone, born of this sacred chamber, can cleanse it.\n"
                "But you must choose wisely when the moment comes. The stone will work "
                "only if your intent is pure — to restore, not to destroy.\n"
                "Take it. And take this warning: there is a Dark Orb in his sanctum. "
                "Should you touch it, the darkness may offer you power... but at a terrible price.'"
            ),
            "has_stone": (
                "'You carry the Purification Stone. Good. Remember — when the moment comes, "
                "choose light over power. The kingdom's soul depends on it.'"
            ),
        },
        "gives_item": "purification_stone",
        "item_given": False,
        "quest_complete": False,
        "current_state": "default",
    },
}

ENEMIES_DATA = {
    "corrupted_wolf": {
        "id": "corrupted_wolf", "name": "Corrupted Wolf", "description": "A wolf with dark ichor seeping from its eyes.",
        "hp": 30, "max_hp": 30, "attack": 8, "defense": 2, "xp_reward": 15, "gold_reward": 5,
        "is_boss": False, "drops": ["health_potion"], "defeated": False,
        "ascii_art": "  /\\_/\\\n ( o.o )\n  > ^ <",
    },
    "dark_goblin": {
        "id": "dark_goblin", "name": "Dark Goblin", "description": "A gnarled goblin wielding a jagged blade.",
        "hp": 25, "max_hp": 25, "attack": 7, "defense": 3, "xp_reward": 12, "gold_reward": 8,
        "is_boss": False, "drops": [], "defeated": False,
        "ascii_art": "  (` ')\n  |   |\n /|___|\\",
    },
    "shadow_bat": {
        "id": "shadow_bat", "name": "Shadow Bat", "description": "A large bat wreathed in dark energy.",
        "hp": 20, "max_hp": 20, "attack": 6, "defense": 1, "xp_reward": 10, "gold_reward": 3,
        "is_boss": False, "drops": [], "defeated": False,
        "ascii_art": " /\\   /\\\n(  ) (  )\n \\\\___//",
    },
    "stone_golem": {
        "id": "stone_golem", "name": "Stone Golem", "description": "A hulking construct of animated rock.",
        "hp": 50, "max_hp": 50, "attack": 12, "defense": 8, "xp_reward": 25, "gold_reward": 15,
        "is_boss": False, "drops": ["elixir_of_strength"], "defeated": False,
        "ascii_art": "  [###]\n [#####]\n  |   |",
    },
    "castle_guard": {
        "id": "castle_guard", "name": "Malachar's Guard", "description": "An armored soldier under Malachar's enchantment.",
        "hp": 40, "max_hp": 40, "attack": 10, "defense": 6, "xp_reward": 20, "gold_reward": 12,
        "is_boss": False, "drops": ["guard_key"], "defeated": False,
        "ascii_art": "  [===]\n  |   |\n /|\\  /|\\",
    },
    # ===== BOSS ENEMIES =====
    "guard_captain": {
        "id": "guard_captain", "name": "Captain Vorn (Boss)", "description": "The former royal guard captain, now Malachar's enforcer. Clad in dark-enchanted armor.",
        "hp": 80, "max_hp": 80, "attack": 15, "defense": 10, "xp_reward": 60, "gold_reward": 30,
        "is_boss": True, "drops": ["dungeon_key", "royal_sword"], "defeated": False,
        "ascii_art": (
            "  +------+\n"
            "  | [**] |\n"
            "  +------+\n"
            "   /|  |\\\n"
            "  / |  | \\\n"
            " /  |  |  \\"
        ),
    },
    "sorcerers_apprentice": {
        "id": "sorcerers_apprentice", "name": "Lyra the Apprentice (Boss)", "description": "Malachar's prodigy, wielding shadow magic with terrifying precision.",
        "hp": 100, "max_hp": 100, "attack": 18, "defense": 8, "xp_reward": 80, "gold_reward": 40,
        "is_boss": True, "drops": ["enchanted_armor", "greater_health_potion"], "defeated": False,
        "ascii_art": (
            "  *  *  *\n"
            " * \\___/ *\n"
            "   |   |\n"
            "   |___|"
        ),
    },
    "dark_sorcerer": {
        "id": "dark_sorcerer", "name": "Malachar the Dark (FINAL BOSS)", "description": "The sorcerer who shattered the kingdom. His robes swirl with shadow energy and his eyes glow crimson.",
        "hp": 150, "max_hp": 150, "attack": 22, "defense": 12, "xp_reward": 200, "gold_reward": 0,
        "is_boss": True, "drops": ["ancient_artifact"], "defeated": False,
        "ascii_art": (
            "    *   *\n"
            "   (>.<)\n"
            "  /|###|\\\n"
            " / |###| \\\n"
            "   |   |\n"
            "  _|___|_"
        ),
    },
}

ROOMS_DATA = {
    "village_entrance": {
        "id": "village_entrance", "name": "Village Entrance",
        "description": (
            "You stand at the crumbling stone gate of the once-proud village of Ashford. "
            "The road ahead splits into the village square. Tall torches flicker weakly "
            "in the unsettling breeze. A rusted sword lies in the dust near the gate post."
        ),
        "ascii_art": (
            "  |    |\n"
            "  |    |\n"
            " /|    |\\\n"
            "/ |    | \\\n"
            "  ========"
        ),
        "exits": {"north": "village_square"},
        "items": ["rusty_sword"],
        "npcs": [], "enemies": [], "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "village_square": {
        "id": "village_square", "name": "Village Square",
        "description": (
            "The village square is eerily quiet. Overturned carts and scattered produce "
            "speak of a hasty evacuation. A wooden signpost points in multiple directions. "
            "To the north, you can see a tavern with a faint warm light. The blacksmith's "
            "forge is to the east, and the old library lies to the west. South leads back to the gate."
        ),
        "ascii_art": (
            "  +---+---+\n"
            "  |  |||  |\n"
            "  |  [ ]  |\n"
            "  +---+---+"
        ),
        "exits": {"south": "village_entrance", "north": "tavern", "east": "blacksmith", "west": "old_library"},
        "items": [], "npcs": [], "enemies": [], "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "tavern": {
        "id": "tavern", "name": "The Weary Boot Tavern",
        "description": (
            "The tavern smells of stale ale and wood smoke. A few candles cast flickering shadows "
            "over empty tables and overturned chairs. The innkeeper Bertha polishes glasses behind "
            "the bar, her expression weary but determined. A health potion sits on the counter, "
            "left behind by a fleeing traveller."
        ),
        "ascii_art": (
            " _________\n"
            "|  TAVERN |\n"
            "|  _   _  |\n"
            "| | | | | |\n"
            "|_|_|_|_|_|"
        ),
        "exits": {"south": "village_square"},
        "items": ["health_potion"],
        "npcs": ["innkeeper_bertha"],
        "enemies": [], "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "blacksmith": {
        "id": "blacksmith", "name": "Garrett's Forge",
        "description": (
            "The forge still burns, casting a ruddy glow. Weapons line the walls — "
            "most confiscated by Malachar's soldiers. The blacksmith Garrett works "
            "stubbornly at his anvil, refusing to stop despite the occupation."
        ),
        "ascii_art": (
            "  /\\/\\/\\\n"
            " | FORGE |\n"
            " |  /\\   |\n"
            " | /  \\  |\n"
            " |______|"
        ),
        "exits": {"west": "village_square"},
        "items": [],
        "npcs": ["blacksmith_garrett"],
        "enemies": [], "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "old_library": {
        "id": "old_library", "name": "The Old Library",
        "description": (
            "Shelves of ancient books line every wall, some floating of their own accord. "
            "Wizard Alara sits at a cluttered desk, surrounded by glowing manuscripts. "
            "An ancient tome rests on the reading podium — it looks important."
        ),
        "ascii_art": (
            " _________\n"
            "| LIBRARY |\n"
            "|||||||||||||\n"
            "| [books] |\n"
            "|_________|"
        ),
        "exits": {"east": "village_square"},
        "items": ["ancient_tome"],
        "npcs": ["wizard_alara"],
        "enemies": [], "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "forest_path": {
        "id": "forest_path", "name": "Forest Path",
        "description": (
            "A dirt trail cuts through dense, twisted trees. The forest feels alive — "
            "and not in a friendly way. Strange growls echo in the dark between the trunks. "
            "A torch has been left jammed in a tree stump. The village is to the south; "
            "the path continues north into the dark forest."
        ),
        "ascii_art": (
            " \\   / \\  /\n"
            "  \\ /   \\/ \n"
            "   |  PATH|\n"
            "   |      |"
        ),
        "exits": {"south": "village_square", "north": "dark_forest"},
        "items": ["torch"],
        "npcs": [],
        "enemies": ["corrupted_wolf"],
        "visited": False, "locked": False, "lock_key": None, "special_action": None,
    },
    "dark_forest": {
        "id": "dark_forest", "name": "The Dark Forest",
        "description": (
            "Twisted trees block out the sky entirely. Glowing eyes watch from the shadows. "
            "The path ahead is nearly invisible without a light source. "
            "You can just make out ancient ruins to the north and the forest path behind you to the south."
        ),
        "ascii_art": (
            " * * * * *\n"
            "  \\|/ \\|/\n"
            "   |   |\n"
            "  /|\\  |"
        ),
        "exits": {"south": "forest_path", "north": "ancient_ruins"},
        "items": [],
        "npcs": [],
        "enemies": ["dark_goblin", "dark_goblin"],
        "visited": False, "locked": False, "lock_key": None, "special_action": None,
    },
    "ancient_ruins": {
        "id": "ancient_ruins", "name": "Ancient Ruins",
        "description": (
            "Crumbling stone columns surround a moss-covered altar. Faded runes still glow "
            "faintly on the stonework. This place predates the kingdom by centuries. "
            "An opening in the floor leads down to underground caves. The dark forest lies south."
        ),
        "ascii_art": (
            " |  | |  |\n"
            " | [=] |  |\n"
            " |     |  |\n"
            "  ~~RUINS~~"
        ),
        "exits": {"south": "dark_forest", "down": "underground_cave"},
        "items": ["health_potion"],
        "npcs": [],
        "enemies": ["stone_golem"],
        "visited": False, "locked": False, "lock_key": None, "special_action": None,
    },
    "underground_cave": {
        "id": "underground_cave", "name": "Underground Cave",
        "description": (
            "Dripping stalactites hang from the ceiling. Bioluminescent fungi cast a pale blue glow "
            "on the wet rock walls. A hand-drawn cave map lies near a dead adventurer's pack. "
            "The ruins are above; a crystal chamber glows to the east."
        ),
        "ascii_art": (
            "  . ' . ' .\n"
            " '  CAVE  '\n"
            "  . [  ] .\n"
            "   '    '"
        ),
        "exits": {"up": "ancient_ruins", "east": "crystal_chamber"},
        "items": ["cave_map"],
        "npcs": [],
        "enemies": ["shadow_bat", "shadow_bat"],
        "visited": False, "locked": False, "lock_key": None, "special_action": None,
    },
    "crystal_chamber": {
        "id": "crystal_chamber", "name": "Crystal Chamber",
        "description": (
            "The chamber is filled with enormous crystals pulsating with soft light. "
            "The air feels charged with ancient magic. The Spirit Guardian manifests here — "
            "a being of pure radiant energy. A crystal shard lies at the base of the largest formation."
        ),
        "ascii_art": (
            "  /\\  /\\\n"
            " /  \\/  \\\n"
            " \\  /\\  /\n"
            "  \\/  \\/"
        ),
        "exits": {"west": "underground_cave"},
        "items": ["crystal_shard"],
        "npcs": ["spirit_guardian"],
        "enemies": [], "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "mountain_pass": {
        "id": "mountain_pass", "name": "Mountain Pass",
        "description": (
            "A treacherous path winds along a clifftop. The wind howls and loose stones "
            "tumble into the void below. A rope lies coiled near a rusted piton in the rock face. "
            "The village is visible far below to the south. The castle's outer walls loom to the north."
        ),
        "ascii_art": (
            " /\\ /\\ /\\\n"
            "/  X  X  \\\n"
            "\\  PATH  /\n"
            " \\/  \\/\\/"
        ),
        "exits": {"south": "village_square", "north": "guard_tower"},
        "items": ["rope"],
        "npcs": [],
        "enemies": ["castle_guard"],
        "visited": False, "locked": False, "lock_key": None, "special_action": None,
    },
    "guard_tower": {
        "id": "guard_tower", "name": "Guard Tower",
        "description": (
            "A stone tower overlooking the approach to the castle. The view from the arrow-slits "
            "reveals the grim state of the kingdom — blighted crops and empty roads. "
            "Castle gates are visible to the north. The pass drops away to the south."
        ),
        "ascii_art": (
            "  +-----+\n"
            "  | [x] |\n"
            "  |     |\n"
            "  |TOWER|\n"
            "  +-----+"
        ),
        "exits": {"south": "mountain_pass", "north": "castle_gates"},
        "items": ["health_potion"],
        "npcs": [],
        "enemies": ["castle_guard"],
        "visited": False, "locked": False, "lock_key": None, "special_action": None,
    },
    "castle_gates": {
        "id": "castle_gates", "name": "Castle Gates",
        "description": (
            "Massive iron-reinforced gates loom before you, marked with Malachar's dark sigil. "
            "The portcullis is raised — an arrogant show of power. Two enchanted guards patrol the entrance. "
            "The courtyard waits beyond. The guard tower is behind you."
        ),
        "ascii_art": (
            " |=======|\n"
            " | GATES |\n"
            " |  |||  |\n"
            " |  |||  |\n"
            " +-------+"
        ),
        "exits": {"south": "guard_tower", "north": "castle_courtyard"},
        "items": [],
        "npcs": [],
        "enemies": ["castle_guard", "castle_guard"],
        "visited": False, "locked": False, "lock_key": None, "special_action": None,
    },
    "castle_courtyard": {
        "id": "castle_courtyard", "name": "Castle Courtyard",
        "description": (
            "The once-beautiful courtyard is now barren and grey. A dead fountain stands at the center. "
            "The throne room entrance is to the north, requiring a guard's key. "
            "The castle gates lie to the south."
        ),
        "ascii_art": (
            " +--+--+--+\n"
            " |  O  O  |\n"
            " |  YARD  |\n"
            " |  O  O  |\n"
            " +--+--+--+"
        ),
        "exits": {"south": "castle_gates", "north": "castle_throne_room"},
        "items": [],
        "npcs": [],
        "enemies": [],
        "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "castle_throne_room": {
        "id": "castle_throne_room", "name": "Throne Room",
        "description": (
            "The grand throne room has been desecrated. The royal tapestries are torn and "
            "replaced with Malachar's dark banners. Captain Vorn stands before the throne, "
            "a twisted knight in service to the sorcerer. A hidden lever is rumored to be "
            "behind the throne. The dungeon entrance is to the east."
        ),
        "ascii_art": (
            " [THRONE ROOM]\n"
            "  |  [T]  |\n"
            "  |       |\n"
            "  +-------+"
        ),
        "exits": {"south": "castle_courtyard", "east": "castle_dungeon"},
        "items": [],
        "npcs": [],
        "enemies": ["guard_captain"],
        "visited": False,
        "locked": True, "lock_key": "guard_key", "special_action": "throne_lever",
    },
    "castle_dungeon": {
        "id": "castle_dungeon", "name": "Castle Dungeon",
        "description": (
            "Damp stone cells stretch into darkness. Chains hang from the walls. "
            "A gaunt prisoner — Theron the steward — peers at you from behind iron bars. "
            "The dungeon key would free him. The throne room is back to the west."
        ),
        "ascii_art": (
            " |=|=|=|=|\n"
            " | DUNGEON|\n"
            " |[CELL]  |\n"
            " |=|=|=|=|"
        ),
        "exits": {"west": "castle_throne_room", "south": "secret_chamber"},
        "items": [],
        "npcs": ["prisoner_theron"],
        "enemies": [],
        "visited": False,
        "locked": False, "lock_key": None, "special_action": "free_prisoner",
    },
    "secret_chamber": {
        "id": "secret_chamber", "name": "Secret Chamber",
        "description": (
            "A hidden room off the dungeon. Malachar uses it to store artifacts too dangerous "
            "even for his sanctum. The Dark Orb pulses malevolently in the center of the room. "
            "A faint glow to the north leads back to the dungeon. The passage to the tower is to the east."
        ),
        "ascii_art": (
            " [SECRET]\n"
            "  | (o) |\n"
            "  |     |\n"
            "  +-----+"
        ),
        "exits": {"north": "castle_dungeon", "east": "dark_tower"},
        "items": ["dark_orb"],
        "npcs": [],
        "enemies": [],
        "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "dark_tower": {
        "id": "dark_tower", "name": "The Dark Tower",
        "description": (
            "A winding staircase ascends through an oppressive darkness. "
            "Shadow energy crackles along the walls. Malachar's apprentice, Lyra, "
            "blocks the way up, her eyes blazing with dark magic. "
            "The secret chamber is accessible to the west. The sanctum awaits above."
        ),
        "ascii_art": (
            "  +-----+\n"
            "  | *** |\n"
            "  | DARK|\n"
            "  |TOWER|\n"
            "  +-----+"
        ),
        "exits": {"west": "secret_chamber", "up": "sorcerers_sanctum"},
        "items": [],
        "npcs": [],
        "enemies": ["sorcerers_apprentice"],
        "visited": False,
        "locked": False, "lock_key": None, "special_action": None,
    },
    "sorcerers_sanctum": {
        "id": "sorcerers_sanctum", "name": "Malachar's Sanctum",
        "description": (
            "The top of the Dark Tower. A circular chamber crackling with dark energy. "
            "At its center hovers the Ancient Artifact — the Heartstone of Aethermoor — "
            "pulsating in a cage of shadow magic. Malachar stands before it, robes swirling, "
            "crimson eyes fixed on you.\n"
            "'So... a hero comes at last. How quaint.'"
        ),
        "ascii_art": (
            " *  *  *  *\n"
            "  SANCTUM\n"
            "   (###)\n"
            " * [ART] *\n"
            "*  *  *  *"
        ),
        "exits": {"down": "dark_tower"},
        "items": [],
        "npcs": [],
        "enemies": ["dark_sorcerer"],
        "visited": False,
        "locked": False, "lock_key": None, "special_action": "final_choice",
    },
}

ACHIEVEMENTS_DATA = [
    {"id": "first_blood", "name": "First Blood", "description": "Win your first combat.", "unlocked": False},
    {"id": "hoarder", "name": "Hoarder", "description": "Carry 8 or more items at once.", "unlocked": False},
    {"id": "diplomat", "name": "Diplomat", "description": "Talk to all 5 NPCs.", "unlocked": False},
    {"id": "explorer", "name": "Explorer", "description": "Visit all 20 rooms.", "unlocked": False},
    {"id": "hero", "name": "Hero of Aethermoor", "description": "Defeat Malachar with the Purification Stone.", "unlocked": False},
    {"id": "fallen_hero", "name": "Fallen Hero", "description": "Accept Malachar's dark pact.", "unlocked": False},
    {"id": "coward", "name": "The One Who Fled", "description": "Escape with the Heartstone.", "unlocked": False},
    {"id": "boss_slayer", "name": "Boss Slayer", "description": "Defeat all 3 boss enemies.", "unlocked": False},
    {"id": "survivalist", "name": "Survivalist", "description": "Reach the final room with full HP.", "unlocked": False},
    {"id": "completionist", "name": "Completionist", "description": "Unlock all other achievements.", "unlocked": False},
]
