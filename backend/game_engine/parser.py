"""
Command parser — tokenizes natural-language commands into (verb, noun, target) tuples.
Supports: go <dir>, take/pick up <item>, drop <item>, use <item> [on <target>],
          talk to <npc>, look/examine <target>, attack <enemy>, flee, inventory,
          stats, help, achievements, equip <item>
"""
from dataclasses import dataclass
from typing import Optional

DIRECTION_ALIASES = {
    "n": "north", "s": "south", "e": "east", "w": "west",
    "u": "up", "d": "down",
    "north": "north", "south": "south", "east": "east", "west": "west",
    "up": "up", "down": "down",
}

GO_VERBS = {"go", "move", "walk", "run", "travel", "head"}
TAKE_VERBS = {"take", "pick", "grab", "get", "collect"}
DROP_VERBS = {"drop", "discard", "leave"}
USE_VERBS = {"use", "apply", "drink", "eat", "consume", "wield"}
TALK_VERBS = {"talk", "speak", "chat", "ask", "greet"}
LOOK_VERBS = {"look", "examine", "inspect", "check", "read", "observe"}
ATTACK_VERBS = {"attack", "fight", "hit", "strike", "stab", "slash", "kill"}
EQUIP_VERBS = {"equip", "wear", "wield"}
HELP_VERBS = {"help", "?", "commands"}
STATS_VERBS = {"stats", "status", "character", "char"}
INV_VERBS = {"inventory", "inv", "i", "bag", "items"}
FLEE_VERBS = {"flee", "run", "escape", "retreat"}
SAVE_VERBS = {"save"}
LOAD_VERBS = {"load"}
ACHIEVEMENTS_VERBS = {"achievements", "ach", "trophies"}

STOP_WORDS = {"to", "the", "a", "an", "at", "with", "on", "up"}


@dataclass
class ParsedCommand:
    verb: str
    noun: Optional[str] = None
    target: Optional[str] = None
    raw: str = ""


def parse(raw: str) -> ParsedCommand:
    tokens = raw.lower().strip().split()
    if not tokens:
        return ParsedCommand(verb="empty", raw=raw)

    filtered = [t for t in tokens if t not in STOP_WORDS]
    if not filtered:
        return ParsedCommand(verb="empty", raw=raw)

    verb_token = filtered[0]
    rest = filtered[1:]

    # Handle direction shortcut (e.g. just "n", "north")
    if verb_token in DIRECTION_ALIASES and not rest:
        return ParsedCommand(verb="go", noun=DIRECTION_ALIASES[verb_token], raw=raw)

    # Detect "pick up" as take
    if verb_token == "pick" and rest and rest[0] == "up":
        rest = rest[1:]
        verb_token = "take"

    # Detect "talk to" pattern in original tokens
    if "talk" in tokens or "speak" in tokens:
        try:
            to_idx = tokens.index("to")
            npc_name = " ".join(tokens[to_idx + 1:])
            return ParsedCommand(verb="talk", noun=npc_name.strip(), raw=raw)
        except ValueError:
            pass

    # Classify verb
    if verb_token in GO_VERBS:
        direction = _extract_direction(rest)
        return ParsedCommand(verb="go", noun=direction, raw=raw)

    if verb_token in TAKE_VERBS:
        return ParsedCommand(verb="take", noun=" ".join(rest) if rest else None, raw=raw)

    if verb_token in DROP_VERBS:
        return ParsedCommand(verb="drop", noun=" ".join(rest) if rest else None, raw=raw)

    if verb_token in USE_VERBS:
        # use <item> on <target>
        if "on" in rest:
            on_idx = rest.index("on")
            noun = " ".join(rest[:on_idx])
            target = " ".join(rest[on_idx + 1:])
            return ParsedCommand(verb="use", noun=noun, target=target, raw=raw)
        return ParsedCommand(verb="use", noun=" ".join(rest) if rest else None, raw=raw)

    if verb_token in TALK_VERBS:
        return ParsedCommand(verb="talk", noun=" ".join(rest) if rest else None, raw=raw)

    if verb_token in LOOK_VERBS:
        return ParsedCommand(verb="look", noun=" ".join(rest) if rest else None, raw=raw)

    if verb_token in ATTACK_VERBS:
        return ParsedCommand(verb="attack", noun=" ".join(rest) if rest else None, raw=raw)

    if verb_token in EQUIP_VERBS:
        return ParsedCommand(verb="equip", noun=" ".join(rest) if rest else None, raw=raw)

    if verb_token in FLEE_VERBS:
        return ParsedCommand(verb="flee", raw=raw)

    if verb_token in HELP_VERBS:
        return ParsedCommand(verb="help", raw=raw)

    if verb_token in STATS_VERBS:
        return ParsedCommand(verb="stats", raw=raw)

    if verb_token in INV_VERBS:
        return ParsedCommand(verb="inventory", raw=raw)

    if verb_token in SAVE_VERBS:
        return ParsedCommand(verb="save", raw=raw)

    if verb_token in LOAD_VERBS:
        return ParsedCommand(verb="load", raw=raw)

    if verb_token in ACHIEVEMENTS_VERBS:
        return ParsedCommand(verb="achievements", raw=raw)

    return ParsedCommand(verb="unknown", noun=" ".join(filtered), raw=raw)


def _extract_direction(tokens: list[str]) -> Optional[str]:
    for t in tokens:
        if t in DIRECTION_ALIASES:
            return DIRECTION_ALIASES[t]
    return None
