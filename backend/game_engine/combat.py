"""Turn-based combat system."""
import random
from typing import Optional
from .models import Player, Enemy


class CombatResult:
    def __init__(self):
        self.messages: list[str] = []
        self.player_won: bool = False
        self.player_died: bool = False
        self.fled: bool = False
        self.xp_gained: int = 0
        self.gold_gained: int = 0
        self.item_drops: list[str] = []
        self.leveled_up: bool = False


class CombatSystem:
    @staticmethod
    def player_attack(player: Player, enemy: Enemy) -> tuple[int, bool]:
        """Returns (damage_dealt, is_critical)."""
        is_crit = random.random() < 0.1
        raw = player.get_attack_power() - enemy.defense + random.randint(1, 6)
        damage = max(1, raw * (2 if is_crit else 1))
        enemy.take_damage(damage)
        return damage, is_crit

    @staticmethod
    def enemy_attack(enemy: Enemy, player: Player) -> int:
        """Returns damage dealt to player."""
        raw = enemy.attack - player.get_defense_power() + random.randint(1, 6)
        damage = max(1, raw)
        player.take_damage(damage)
        return damage

    @staticmethod
    def attempt_flee() -> bool:
        """50% chance to successfully flee."""
        return random.random() < 0.5

    @classmethod
    def resolve_attack(cls, player: Player, enemy: Enemy) -> CombatResult:
        """Player attacks, then enemy retaliates if still alive."""
        result = CombatResult()

        # Player attacks
        dmg, crit = cls.player_attack(player, enemy)
        crit_str = " CRITICAL HIT!" if crit else ""
        result.messages.append(
            f"⚔️  You strike {enemy.name} for {dmg} damage!{crit_str} "
            f"({enemy.hp}/{enemy.max_hp} HP remaining)"
        )

        if not enemy.is_alive():
            result.player_won = True
            result.xp_gained = enemy.xp_reward
            result.gold_gained = enemy.gold_reward
            result.item_drops = enemy.drops[:]
            enemy.defeated = True
            result.messages.append(
                f"☠️  {enemy.name} has been defeated! "
                f"You gain {enemy.xp_reward} XP and {enemy.gold_reward} gold."
            )
            if enemy.drops:
                result.messages.append(f"💎 Items dropped: {', '.join(enemy.drops)}")
            return result

        # Enemy retaliates
        edamg = cls.enemy_attack(enemy, player)
        result.messages.append(
            f"💥 {enemy.name} strikes back for {edamg} damage! "
            f"(Your HP: {player.hp}/{player.max_hp})"
        )

        if not player.is_alive():
            result.player_died = True
            result.messages.append("💀 You have been slain...")

        return result

    @classmethod
    def resolve_flee(cls, player: Player, enemy: Enemy) -> CombatResult:
        result = CombatResult()
        if cls.attempt_flee():
            result.fled = True
            result.messages.append("🏃 You manage to escape!")
        else:
            edamg = cls.enemy_attack(enemy, player)
            result.messages.append(
                f"❌ You fail to escape! {enemy.name} hits you for {edamg} damage! "
                f"(Your HP: {player.hp}/{player.max_hp})"
            )
            if not player.is_alive():
                result.player_died = True
                result.messages.append("💀 You have been slain...")
        return result
