# Aethermoor — Text-Based Adventure Game

A fully featured, terminal-style text-based adventure game built with a Python OOP game engine, FastAPI REST backend, PostgreSQL persistence, and a React/TypeScript frontend with CRT-green terminal aesthetics.

---

## Features

- **20-room interconnected world** — villages, forests, dungeons, ruins, a dark tower, and a sorcerer's sanctum
- **Turn-based combat** — attack, flee, crits, XP, leveling, loot drops
- **3 story endings** — Hero's Triumph, Dark Pact, The One Who Fled
- **10 achievements** — unlocked automatically as you play
- **Full auto-save** — game state persisted to PostgreSQL after every command
- **Command history** — navigate previous commands with ↑ / ↓ arrow keys
- **CRT terminal UI** — scanline overlay, Fira Code font, color-coded output

---

## Tech Stack

| Layer | Technology |
|---|---|
| Game Engine | Python 3.12, OOP dataclasses |
| API | FastAPI + Uvicorn |
| Database | PostgreSQL 16 + SQLAlchemy 2 |
| Frontend | React 18 + TypeScript + Vite |
| Styling | Pure inline styles, CRT aesthetic |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
Text-Based Adventure/
├── backend/
│   ├── game_engine/
│   │   ├── models.py        # Item, NPC, Enemy, Room, Player dataclasses
│   │   ├── world_data.py    # All static content (20 rooms, items, NPCs, enemies)
│   │   ├── world.py         # World class — builds and serializes game objects
│   │   ├── combat.py        # CombatSystem — attack/flee resolution
│   │   ├── parser.py        # Natural language command tokenizer
│   │   └── game_session.py  # GameSession — command dispatch and story logic
│   ├── database/
│   │   ├── database.py      # SQLAlchemy engine and session factory
│   │   └── models.py        # GameStateDB ORM model
│   ├── routers/
│   │   └── game.py          # FastAPI route handlers
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── types/           # TypeScript interfaces
│   │   ├── hooks/useGame.ts # All game state logic
│   │   ├── services/api.ts  # Axios API client
│   │   └── components/
│   │       ├── StartScreen.tsx
│   │       ├── OutputDisplay.tsx
│   │       ├── CommandInput.tsx
│   │       └── Sidebar.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Setup & Running

### Option A — Docker Compose (recommended)

```bash
docker compose up --build
```

- Frontend: http://localhost:4000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Option B — Local development

**Prerequisites:** Python 3.12, Node 20, PostgreSQL 16

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL and create the database
psql -U postgres -c "CREATE DATABASE aethermoor;"

# Copy env and start
cp .env.example .env            # edit DATABASE_URL if needed
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:4000.

---

## REST API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/game/new` | Start a new game (`{ "player_name": "..." }`) |
| GET | `/game/{id}` | Load existing session |
| POST | `/game/{id}/command` | Send a command (`{ "command": "..." }`) |
| GET | `/game/{id}/achievements` | List all achievements |
| DELETE | `/game/{id}` | Delete a session |

---

## Game Commands

| Command | Description |
|---|---|
| `go <direction>` / `north` / `n` | Move between rooms |
| `look` | Describe the current room |
| `take <item>` | Pick up an item |
| `drop <item>` | Drop an item from inventory |
| `use <item>` | Use an item |
| `use <item> on <target>` | Use an item on a specific target |
| `equip <item>` | Equip a weapon or armor |
| `inventory` / `i` | Show your inventory |
| `stats` | Show player statistics |
| `attack` / `fight` | Attack an enemy in the room |
| `flee` / `run` | Attempt to escape combat (50% chance) |
| `talk to <npc>` | Speak with an NPC |
| `achievements` | View achievement progress |
| `help` | List all commands |

**Directions:** `north`, `south`, `east`, `west`, `up`, `down` (or single letters `n`, `s`, `e`, `w`, `u`, `d`)

---

## World Map

```
Village Entrance
     │
Village Square ────── Tavern
     │                  │
     ├── Blacksmith   (inn)
     │
     ├── Old Library
     │
     ├── Mountain Pass
     │        │
     │   Guard Tower
     │        │
     │   Castle Gates
     │        │
     │   Castle Courtyard
     │        │
     │   Castle Throne Room
     │        │
     │   Castle Dungeon ── Secret Chamber
     │                          │
     │                     Dark Tower
     │                          │
     │                   Sorcerer's Sanctum
     │
     └── Forest Path
              │
         Dark Forest
              │
        Ancient Ruins
              │
       Underground Cave
              │
        Crystal Chamber
```

---

## Story & Endings

The sorcerer **Malachar** has seized the castle and corrupted the **Heartstone of Aethermoor**. As the last adventurer, you must stop him.

| Ending | How to unlock |
|---|---|
| **Hero's Triumph** | Obtain the Purification Stone → use it on Malachar in the Sanctum |
| **Dark Pact** | Obtain the Dark Orb → use it on Malachar in the Sanctum |
| **The One Who Fled** | Use the `flee` command to escape the world entirely |

---

## Achievements

| ID | Name | How to unlock |
|---|---|---|
| `first_blood` | First Blood | Win your first combat |
| `hoarder` | Hoarder | Carry 5 or more items |
| `diplomat` | Diplomat | Talk to 3 different NPCs |
| `explorer` | Explorer | Visit 10 or more rooms |
| `hero` | Hero of Aethermoor | Complete the Hero's Triumph ending |
| `fallen_hero` | Fallen Hero | Complete the Dark Pact ending |
| `coward` | The One Who Fled | Use the escape ending |
| `boss_slayer` | Boss Slayer | Defeat all 3 bosses |
| `survivalist` | Survivalist | Survive with 5 HP or less |
| `completionist` | Completionist | Unlock all other 9 achievements |

---

## Combat Mechanics

- **Damage formula:** `attacker.attack − defender.defense + random(1, 6)` (minimum 1)
- **Crit chance:** 10% — doubles the damage roll
- **Flee:** 50% success; on failure the enemy gets a free attack
- **XP and leveling:** Defeating enemies grants XP; level-up raises max HP, attack, and defense
- **Loot:** Enemies may drop items into the room on death

---

## Architecture

```
Browser (React)
    │  HTTP (Vite proxy → port 8000)
    ▼
FastAPI (Uvicorn)
    │  SQLAlchemy
    ▼
PostgreSQL ── stores full JSON game state blob per session
    
GameSession (in-memory per request)
    ├── World  (rooms, items, NPCs, enemies)
    ├── Player
    ├── CombatSystem
    └── Parser
```

Game state is fully serialized via `to_dict()` / `from_dict()` on every command, so every request is stateless at the API layer — the database is the single source of truth.

---

## Development Notes

- **No mocking**: All tests should hit a real PostgreSQL instance — mock/prod divergence has caused issues before.
- **Auto-save**: The session is written back to the database after every command, so no explicit save action is needed.
- **Session ID**: Stored in `localStorage` so the browser can resume a game after a page refresh.
