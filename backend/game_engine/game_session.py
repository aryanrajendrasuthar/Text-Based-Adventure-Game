"""
GameSession — orchestrates the entire game state and command processing.
"""
import copy
from typing import Optional
from .models import Player, Item
from .world import World
from .combat import CombatSystem, CombatResult
from .parser import ParsedCommand, parse


HELP_TEXT = """
╔══════════════════════════════════════════════════╗
║              COMMAND REFERENCE                   ║
╠══════════════════════════════════════════════════╣
║  go <direction>   Move (north/south/east/west/   ║
║                   up/down). Shortcut: n/s/e/w/u/d║
║  look             Describe current room          ║
║  look <object>    Examine something              ║
║  take <item>      Pick up an item                ║
║  drop <item>      Drop an item                   ║
║  use <item>       Use an item                    ║
║  use <item> on    Use item on a target           ║
║    <target>                                      ║
║  equip <item>     Equip weapon or armor          ║
║  inventory (i)    List carried items             ║
║  stats            Show player stats              ║
║  talk to <npc>    Speak with an NPC              ║
║  attack <enemy>   Attack a monster               ║
║  flee             Attempt to flee combat         ║
║  achievements     View achievement progress      ║
║  save             Save the game                  ║
║  help             Show this screen               ║
╚══════════════════════════════════════════════════╝
"""


class GameSession:
    def __init__(self, player_name: str):
        self.player = Player(name=player_name)
        self.world = World()
        self.command_count: int = 0
        self.npcs_spoken_to: set[str] = set()
        self.bosses_defeated: int = 0
        self.combat_wins: int = 0
        self.game_over: bool = False
        self.ending: Optional[str] = None  # "hero", "dark_pact", "escape"
        # Track active combat (only one enemy at a time)
        self.active_enemy_id: Optional[str] = None

    # ─────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────

    def process_command(self, raw: str) -> dict:
        """Entry point. Returns {messages: [...], state: {...}}"""
        if self.game_over:
            return self._respond(["The adventure has ended. Start a new game to play again."])

        self.command_count += 1
        cmd = parse(raw)

        dispatch = {
            "go": self._cmd_go,
            "look": self._cmd_look,
            "take": self._cmd_take,
            "drop": self._cmd_drop,
            "use": self._cmd_use,
            "equip": self._cmd_equip,
            "talk": self._cmd_talk,
            "attack": self._cmd_attack,
            "flee": self._cmd_flee,
            "inventory": self._cmd_inventory,
            "stats": self._cmd_stats,
            "achievements": self._cmd_achievements,
            "help": lambda c: [HELP_TEXT],
            "save": lambda c: ["Use the save button in the sidebar to save your game."],
            "empty": lambda c: ["Please enter a command. Type 'help' for a list of commands."],
            "unknown": self._cmd_unknown,
        }

        handler = dispatch.get(cmd.verb, self._cmd_unknown)
        messages = handler(cmd)

        # Achievement checks (passive)
        ach_msgs = self._check_achievements()
        messages.extend(ach_msgs)

        return self._respond(messages)

    # ─────────────────────────────────────────────────────────
    # Command handlers
    # ─────────────────────────────────────────────────────────

    def _cmd_go(self, cmd: ParsedCommand) -> list[str]:
        if not cmd.noun:
            return ["Go where? Specify a direction: north, south, east, west, up, down."]

        direction = cmd.noun
        room = self.world.get_room(self.player.current_room)
        if direction not in room.exits:
            return [f"You can't go {direction} from here."]

        target_id = room.exits[direction]
        target_room = self.world.get_room(target_id)

        if target_room.locked:
            key_item = self.world.get_item(target_room.lock_key)
            if target_room.lock_key in self.player.inventory:
                target_room.locked = False
                msgs = [f"🔑 You use the {key_item.name} to unlock the door."]
            else:
                name = key_item.name if key_item else "a key"
                return [f"🔒 The way is locked. You need {name} to proceed."]
        else:
            msgs = []

        # Check for enemies blocking the path
        alive_enemies = self._get_alive_enemies_in_room(self.player.current_room)
        if alive_enemies:
            names = ", ".join(e.name for e in alive_enemies)
            return [f"⚠️  You can't leave while enemies are present! ({names})"]

        self.player.current_room = target_id
        if not target_room.visited:
            target_room.visited = True
            msgs.extend(self._describe_room(target_room, full=True))
        else:
            msgs.extend(self._describe_room(target_room, full=False))

        return msgs

    def _cmd_look(self, cmd: ParsedCommand) -> list[str]:
        room = self.world.get_room(self.player.current_room)

        if not cmd.noun:
            return self._describe_room(room, full=True)

        noun = cmd.noun.lower()

        # Look at item in room or inventory
        for iid in room.items + self.player.inventory:
            item = self.world.get_item(iid)
            if item and noun in item.name.lower():
                return [f"[{item.name}]\n{item.description}"]

        # Look at NPC
        for nid in room.npcs:
            npc = self.world.get_npc(nid)
            if npc and noun in npc.name.lower():
                return [f"[{npc.name}]\n{npc.description}"]

        # Look at enemy
        for eid in room.enemies:
            enemy = self.world.get_enemy(eid)
            if enemy and not enemy.defeated and noun in enemy.name.lower():
                return [
                    f"[{enemy.name}]\n{enemy.description}\n"
                    f"{enemy.ascii_art}\n"
                    f"HP: {enemy.hp}/{enemy.max_hp} | ATK: {enemy.attack} | DEF: {enemy.defense}"
                ]

        return [f"You don't see '{cmd.noun}' here."]

    def _cmd_take(self, cmd: ParsedCommand) -> list[str]:
        if not cmd.noun:
            return ["Take what?"]

        noun = cmd.noun.lower()
        room = self.world.get_room(self.player.current_room)

        for iid in list(room.items):
            item = self.world.get_item(iid)
            if item and noun in item.name.lower():
                room.items.remove(iid)
                # Handle stackable items (health potions)
                if iid in self.player.inventory:
                    existing = self.world.get_item(iid)
                    existing.quantity += 1
                else:
                    self.player.inventory.append(iid)
                return [f"✅ You pick up the {item.name}."]

        return [f"There is no '{cmd.noun}' here to take."]

    def _cmd_drop(self, cmd: ParsedCommand) -> list[str]:
        if not cmd.noun:
            return ["Drop what?"]

        noun = cmd.noun.lower()
        room = self.world.get_room(self.player.current_room)

        for iid in list(self.player.inventory):
            item = self.world.get_item(iid)
            if item and noun in item.name.lower():
                self.player.inventory.remove(iid)
                room.items.append(iid)
                return [f"You drop the {item.name}."]

        return [f"You don't have '{cmd.noun}'."]

    def _cmd_use(self, cmd: ParsedCommand) -> list[str]:
        if not cmd.noun:
            return ["Use what?"]

        noun = cmd.noun.lower()
        item_id = self._find_item_in_inventory(noun)
        if not item_id:
            return [f"You don't have '{cmd.noun}'."]

        item = self.world.get_item(item_id)
        target = (cmd.target or "").lower()

        # Consumables
        if item.item_type == "consumable":
            return self._use_consumable(item_id, item)

        # Quest items — context-sensitive
        if item.item_type == "quest":
            return self._use_quest_item(item_id, item, target)

        # Keys — handled contextually
        if item.item_type == "key":
            return [f"The {item.name} will be used automatically when needed."]

        return [f"You're not sure how to use the {item.name} right now."]

    def _use_consumable(self, item_id: str, item: Item) -> list[str]:
        msgs = []
        if item.item_type == "consumable":
            if item_id == "elixir_of_strength":
                self.player.attack += item.effect
                msgs.append(f"⚡ You drink the {item.name}! Your attack permanently increases by {item.effect}.")
            else:
                healed = self.player.heal(item.effect)
                msgs.append(f"💊 You use the {item.name}. You recover {healed} HP. ({self.player.hp}/{self.player.max_hp})")

            item.quantity -= 1
            if item.quantity <= 0:
                self.player.inventory.remove(item_id)
        return msgs

    def _use_quest_item(self, item_id: str, item: Item, target: str) -> list[str]:
        room = self.world.get_room(self.player.current_room)

        # Ancient tome with wizard
        if item_id == "ancient_tome" and room.id == "old_library":
            wizard = self.world.get_npc("wizard_alara")
            if wizard:
                wizard.current_state = "has_tome"
                bertha = self.world.get_npc("innkeeper_bertha")
                if bertha:
                    bertha.current_state = "has_tome"
                self.player.flags["gave_tome"] = True
                return [
                    "📖 You hand the Ancient Tome to Alara.\n" + wizard.get_dialogue()
                ]

        # Purification stone on dark sorcerer
        if item_id == "purification_stone" and "malachar" in target:
            enemy = self.world.get_enemy("dark_sorcerer")
            if room.id == "sorcerers_sanctum" and enemy and not enemy.defeated:
                return self._ending_hero()
            return ["The stone has no effect here."]

        # Dark orb — offer to sorcerer (dark ending)
        if item_id == "dark_orb" and "malachar" in target:
            enemy = self.world.get_enemy("dark_sorcerer")
            if room.id == "sorcerers_sanctum" and enemy and not enemy.defeated:
                return self._ending_dark_pact()
            return ["There is no one to give it to here."]

        # Ancient artifact — try to escape
        if item_id == "ancient_artifact":
            return ["The Heartstone pulses warmly in your hands. You sense it must be returned to the kingdom's heart."]

        return [f"You hold up the {item.name} but nothing special happens right now."]

    def _cmd_equip(self, cmd: ParsedCommand) -> list[str]:
        if not cmd.noun:
            return ["Equip what?"]

        noun = cmd.noun.lower()
        item_id = self._find_item_in_inventory(noun)
        if not item_id:
            return [f"You don't have '{cmd.noun}'."]

        item = self.world.get_item(item_id)
        if item.item_type == "weapon":
            # Unequip old weapon bonus
            if self.player.equipped_weapon:
                old = self.world.get_item(self.player.equipped_weapon)
                if old:
                    self.player.attack -= old.effect
            self.player.equipped_weapon = item_id
            self.player.attack += item.effect
            return [f"⚔️  You equip the {item.name}. Attack power increases by {item.effect}."]

        if item.item_type == "armor":
            if self.player.equipped_armor:
                old = self.world.get_item(self.player.equipped_armor)
                if old:
                    self.player.defense -= old.effect
            self.player.equipped_armor = item_id
            self.player.defense += item.effect
            return [f"🛡️  You equip the {item.name}. Defense increases by {item.effect}."]

        return [f"The {item.name} cannot be equipped."]

    def _cmd_talk(self, cmd: ParsedCommand) -> list[str]:
        if not cmd.noun:
            return ["Talk to whom?"]

        noun = cmd.noun.lower()
        room = self.world.get_room(self.player.current_room)

        for nid in room.npcs:
            npc = self.world.get_npc(nid)
            if npc and noun in npc.name.lower():
                self.npcs_spoken_to.add(nid)
                msgs = [f"\n💬 [{npc.name}]\n{npc.get_dialogue()}"]

                # Auto-give item if not yet given
                if npc.gives_item and not npc.item_given:
                    gift_item = self.world.get_item(npc.gives_item)
                    if gift_item:
                        self.player.inventory.append(npc.gives_item)
                        npc.item_given = True
                        msgs.append(f"\n🎁 {npc.name} gives you: {gift_item.name}")

                # Special: free prisoner with dungeon key
                if nid == "prisoner_theron" and "dungeon_key" in self.player.inventory:
                    npc.current_state = "freed"
                    self.player.flags["freed_theron"] = True
                    msgs = [f"\n💬 [{npc.name}]\n{npc.get_dialogue()}"]

                # Alara with tome
                if nid == "wizard_alara" and self.player.flags.get("gave_tome"):
                    npc.current_state = "has_tome"

                return msgs

        return [f"There's nobody named '{cmd.noun}' here to talk to."]

    def _cmd_attack(self, cmd: ParsedCommand) -> list[str]:
        room = self.world.get_room(self.player.current_room)
        alive_enemies = self._get_alive_enemies_in_room(self.player.current_room)

        if not alive_enemies:
            return ["There are no enemies here to fight."]

        # Select target
        if cmd.noun:
            noun = cmd.noun.lower()
            target_enemy = next((e for e in alive_enemies if noun in e.name.lower()), None)
            if not target_enemy:
                return [f"There is no enemy called '{cmd.noun}' here."]
        else:
            target_enemy = alive_enemies[0]

        self.active_enemy_id = target_enemy.id
        result = CombatSystem.resolve_attack(self.player, target_enemy)
        msgs = result.messages[:]

        if result.player_won:
            self.combat_wins += 1
            self.active_enemy_id = None
            if target_enemy.is_boss:
                self.bosses_defeated += 1
                self.player.flags[f"defeated_{target_enemy.id}"] = True
                if target_enemy.id == "guard_captain":
                    # Update blacksmith dialogue
                    bs = self.world.get_npc("blacksmith_garrett")
                    if bs:
                        bs.current_state = "after_boss1"
                if target_enemy.id == "dark_sorcerer":
                    return msgs + self._ending_hero_combat()

            leveled = self.player.gain_xp(result.xp_gained)
            self.player.gold += result.gold_gained
            if leveled:
                msgs.append(
                    f"🎉 LEVEL UP! You are now level {self.player.level}! "
                    f"Max HP +20, Attack +3, Defense +2."
                )

            # Drop items into room
            for drop_id in result.item_drops:
                if drop_id not in room.items:
                    room.items.append(drop_id)
            if result.item_drops:
                drops = [self.world.get_item(d).name for d in result.item_drops if self.world.get_item(d)]
                msgs.append(f"💎 {target_enemy.name} dropped: {', '.join(drops)}")

        elif result.player_died:
            self.game_over = True
            self.ending = "death"
            msgs.append(
                "\n═══════════════════════════════\n"
                "GAME OVER — You have fallen.\n"
                "═══════════════════════════════\n"
                "Your legend ends here, brave adventurer."
            )

        return msgs

    def _cmd_flee(self, cmd: ParsedCommand) -> list[str]:
        alive_enemies = self._get_alive_enemies_in_room(self.player.current_room)
        if not alive_enemies:
            return ["There's nothing to flee from."]

        enemy = alive_enemies[0]
        result = CombatSystem.resolve_flee(self.player, enemy)
        msgs = result.messages[:]

        if result.fled:
            # Move player back one step (to previous room via first available exit going south/west/down)
            room = self.world.get_room(self.player.current_room)
            retreat = None
            for d in ["south", "west", "down", "north", "east", "up"]:
                if d in room.exits:
                    retreat = room.exits[d]
                    break
            if retreat:
                self.player.current_room = retreat
                msgs.append(f"You flee to {self.world.get_room(retreat).name}.")

        elif result.player_died:
            self.game_over = True
            self.ending = "death"
            msgs.append(
                "\n═══════════════════════════════\n"
                "GAME OVER — You have fallen.\n"
                "═══════════════════════════════"
            )

        return msgs

    def _cmd_inventory(self, cmd: ParsedCommand) -> list[str]:
        if not self.player.inventory:
            return ["Your inventory is empty."]

        lines = ["📦 INVENTORY:"]
        for iid in self.player.inventory:
            item = self.world.get_item(iid)
            if item:
                qty = f" x{item.quantity}" if item.quantity > 1 else ""
                equipped = ""
                if iid == self.player.equipped_weapon:
                    equipped = " [EQUIPPED - Weapon]"
                elif iid == self.player.equipped_armor:
                    equipped = " [EQUIPPED - Armor]"
                lines.append(f"  • {item.name}{qty}{equipped} — {item.description[:50]}...")
        return ["\n".join(lines)]

    def _cmd_stats(self, cmd: ParsedCommand) -> list[str]:
        p = self.player
        hp_bar = self._make_bar(p.hp, p.max_hp, 20)
        xp_needed = p.level * 50
        xp_bar = self._make_bar(p.xp % xp_needed, xp_needed, 20)
        weapon = self.world.get_item(p.equipped_weapon).name if p.equipped_weapon else "None"
        armor = self.world.get_item(p.equipped_armor).name if p.equipped_armor else "None"
        return [
            f"╔══════════════════════════╗\n"
            f"║  {p.name[:22]:<22}  ║\n"
            f"╠══════════════════════════╣\n"
            f"║  Level    : {p.level:<14}║\n"
            f"║  HP       : [{hp_bar}] {p.hp}/{p.max_hp}\n"
            f"║  XP       : [{xp_bar}] {p.xp % xp_needed}/{xp_needed}\n"
            f"║  Attack   : {p.attack:<14}║\n"
            f"║  Defense  : {p.defense:<14}║\n"
            f"║  Gold     : {p.gold:<14}║\n"
            f"║  Weapon   : {weapon[:14]:<14}║\n"
            f"║  Armor    : {armor[:14]:<14}║\n"
            f"╚══════════════════════════╝"
        ]

    def _cmd_achievements(self, cmd: ParsedCommand) -> list[str]:
        lines = ["🏆 ACHIEVEMENTS:"]
        for a in self.world.achievements:
            icon = "✅" if a["unlocked"] else "🔒"
            name = a["name"] if a["unlocked"] else "???"
            desc = a["description"] if a["unlocked"] else "???"
            lines.append(f"  {icon} {name}: {desc}")
        return ["\n".join(lines)]

    def _cmd_unknown(self, cmd: ParsedCommand) -> list[str]:
        return [
            f"I don't understand '{cmd.raw}'. Type 'help' to see available commands."
        ]

    # ─────────────────────────────────────────────────────────
    # Endings
    # ─────────────────────────────────────────────────────────

    def _ending_hero(self) -> list[str]:
        """Use purification stone on Malachar — Hero ending."""
        enemy = self.world.get_enemy("dark_sorcerer")
        enemy.defeated = True
        self.game_over = True
        self.ending = "hero"
        self.world.unlock_achievement("hero")
        # Add artifact to inventory
        self.player.inventory.append("ancient_artifact")
        return [
            "\n" + "═" * 50,
            "✨ HERO'S TRIUMPH ✨",
            "═" * 50,
            "You raise the Purification Stone and speak the binding words:\n"
            "'By light of truth and will unbound, let darkness fail and hope be found.'\n\n"
            "The stone blazes with blinding white light. Malachar screams as the dark magic "
            "is ripped from him. The shadows dissolve. The Heartstone breaks free of its cage "
            "and floats into your hands, warm and pulsing with life.\n\n"
            "Malachar collapses — a broken old man, stripped of his power. The kingdom shudders, "
            "then breathes again. Birds sing. Crops straighten. Light returns to Aethermoor.\n\n"
            "You descend from the tower to cheering villagers. The king is found alive in the dungeon. "
            "Bards will sing of the hero who saved Aethermoor for generations to come.\n\n"
            "🎉 CONGRATULATIONS! You have achieved the TRUE ENDING.",
            "═" * 50,
        ]

    def _ending_hero_combat(self) -> list[str]:
        """Beat Malachar in straight combat — still hero ending but harder way."""
        self.game_over = True
        self.ending = "hero"
        self.world.unlock_achievement("hero")
        return [
            "\n" + "═" * 50,
            "⚔️  VICTORY THROUGH STRENGTH ⚔️",
            "═" * 50,
            "Malachar falls, his dark magic sputtering out like a candle in the wind. "
            "With his defeat, the shadow curse begins to lift across Aethermoor. "
            "The Heartstone pulses as its corruption fades.\n\n"
            "You carry the artifact down from the tower. The kingdom lives again.\n\n"
            "🎉 CONGRATULATIONS! A hard-won victory for Aethermoor.",
            "═" * 50,
        ]

    def _ending_dark_pact(self) -> list[str]:
        """Give dark orb to Malachar — dark pact ending."""
        self.game_over = True
        self.ending = "dark_pact"
        self.world.unlock_achievement("fallen_hero")
        return [
            "\n" + "═" * 50,
            "🌑 THE DARK PACT 🌑",
            "═" * 50,
            "You hold out the Dark Orb. Malachar's eyes widen, then curve into a slow smile.\n\n"
            "'Clever... very clever. You've brought me the missing piece.'\n\n"
            "He takes the orb and melds it with the Heartstone. The chamber floods with shadow. "
            "A crown materializes above your head.\n\n"
            "'Rule at my side,' he says. 'Together we will reshape this world.'\n\n"
            "You accept. Aethermoor falls fully into darkness. The villagers who believed in you "
            "are enslaved. Bertha's kind face haunts your dreams — but you tell yourself power was worth it.\n\n"
            "💀 THE END — You chose power over light.",
            "═" * 50,
        ]

    def ending_escape(self) -> list[str]:
        """Player escapes with the artifact but leaves everyone behind."""
        self.game_over = True
        self.ending = "escape"
        self.world.unlock_achievement("coward")
        return [
            "\n" + "═" * 50,
            "🌙 THE ONE WHO FLED 🌙",
            "═" * 50,
            "With Theron's map in hand, you find the hidden passage and slip out of the castle "
            "before Malachar realizes what has happened.\n\n"
            "The Heartstone is safe — in your hands, far from Aethermoor. You tell yourself "
            "you'll return someday. That you'll find help. That this is temporary.\n\n"
            "The kingdom sinks deeper into shadow behind you. Bertha, Alara, Garrett... "
            "all lost. You escape to freedom, but some nights the weight of what you left "
            "behind is heavier than any armor.\n\n"
            "🌙 THE END — You escaped, but at what cost?",
            "═" * 50,
        ]

    # ─────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────

    def _describe_room(self, room, full: bool = True) -> list[str]:
        msgs = [f"\n{'═' * 40}\n📍 {room.name}\n{'═' * 40}"]

        if room.ascii_art:
            msgs.append(room.ascii_art)

        if full:
            msgs.append(room.description)

        # Exits
        exit_strs = [f"{d} → {self.world.get_room(rid).name}" for d, rid in room.exits.items()]
        msgs.append(f"🚪 Exits: {', '.join(exit_strs)}")

        # Items
        alive_items = [iid for iid in room.items]
        if alive_items:
            item_names = [self.world.get_item(i).name for i in alive_items if self.world.get_item(i)]
            msgs.append(f"📦 Items: {', '.join(item_names)}")

        # NPCs
        if room.npcs:
            npc_names = [self.world.get_npc(n).name for n in room.npcs if self.world.get_npc(n)]
            msgs.append(f"👤 People: {', '.join(npc_names)}")

        # Enemies
        alive = self._get_alive_enemies_in_room(room.id)
        if alive:
            enemy_descs = [f"{e.name} (HP: {e.hp}/{e.max_hp})" for e in alive]
            msgs.append(f"⚔️  Enemies: {', '.join(enemy_descs)}")

        return msgs

    def _get_alive_enemies_in_room(self, room_id: str) -> list:
        room = self.world.get_room(room_id)
        result = []
        seen = set()
        for eid in room.enemies:
            if eid in seen:
                continue
            seen.add(eid)
            enemy = self.world.get_enemy(eid)
            if enemy and not enemy.defeated:
                result.append(enemy)
        return result

    def _find_item_in_inventory(self, noun: str) -> Optional[str]:
        for iid in self.player.inventory:
            item = self.world.get_item(iid)
            if item and noun in item.name.lower():
                return iid
        return None

    def _make_bar(self, current: int, maximum: int, length: int) -> str:
        filled = int((current / max(1, maximum)) * length)
        return "█" * filled + "░" * (length - filled)

    def _check_achievements(self) -> list[str]:
        msgs = []

        def unlock(ach_id: str):
            name = self.world.unlock_achievement(ach_id)
            if name:
                msgs.append(f"\n🏆 ACHIEVEMENT UNLOCKED: {name}!")

        if self.combat_wins >= 1:
            unlock("first_blood")
        if len(self.player.inventory) >= 8:
            unlock("hoarder")
        if len(self.npcs_spoken_to) >= 5:
            unlock("diplomat")
        if all(r.visited for r in self.world.rooms.values()):
            unlock("explorer")
        if self.bosses_defeated >= 3:
            unlock("boss_slayer")
        if self.player.hp == self.player.max_hp and self.player.current_room == "sorcerers_sanctum":
            unlock("survivalist")

        return msgs

    # ─────────────────────────────────────────────────────────
    # Serialization
    # ─────────────────────────────────────────────────────────

    def _respond(self, messages: list[str]) -> dict:
        return {
            "messages": messages,
            "state": self.get_state(),
        }

    def get_state(self) -> dict:
        room = self.world.get_room(self.player.current_room)
        alive_enemies = self._get_alive_enemies_in_room(self.player.current_room)
        return {
            "player": self.player.to_dict(),
            "current_room": room.to_dict() if room else None,
            "alive_enemies": [e.to_dict() for e in alive_enemies],
            "achievements": self.world.achievements,
            "game_over": self.game_over,
            "ending": self.ending,
            "command_count": self.command_count,
            "bosses_defeated": self.bosses_defeated,
        }

    def to_dict(self) -> dict:
        return {
            "player": self.player.to_dict(),
            "world": self.world.to_dict(),
            "command_count": self.command_count,
            "npcs_spoken_to": list(self.npcs_spoken_to),
            "bosses_defeated": self.bosses_defeated,
            "combat_wins": self.combat_wins,
            "game_over": self.game_over,
            "ending": self.ending,
            "active_enemy_id": self.active_enemy_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameSession":
        session = cls.__new__(cls)
        session.player = Player.from_dict(data["player"])
        session.world = World.from_dict(data["world"])
        session.command_count = data.get("command_count", 0)
        session.npcs_spoken_to = set(data.get("npcs_spoken_to", []))
        session.bosses_defeated = data.get("bosses_defeated", 0)
        session.combat_wins = data.get("combat_wins", 0)
        session.game_over = data.get("game_over", False)
        session.ending = data.get("ending")
        session.active_enemy_id = data.get("active_enemy_id")
        return session

    def get_intro(self) -> dict:
        """Return the opening narrative and first room description."""
        intro = [
            "═" * 50,
            "   THE LOST KINGDOM OF AETHERMOOR",
            "═" * 50,
            f"\nWelcome, {self.player.name}.\n",
            "The kingdom of Aethermoor has fallen under a shadow. "
            "Malachar, a rogue sorcerer, has seized the castle and corrupted the ancient Heartstone — "
            "the source of the kingdom's life. The king has vanished. The people are in despair.\n",
            "You arrive as a wandering adventurer, drawn by rumours of chaos and a kingdom in need. "
            "Whether you save it, exploit it, or simply survive... is up to you.\n",
            "Type 'help' at any time to see available commands.\n",
            "═" * 50,
        ]
        room = self.world.get_room(self.player.current_room)
        room.visited = True
        intro.extend(self._describe_room(room, full=True))
        return self._respond(intro)
