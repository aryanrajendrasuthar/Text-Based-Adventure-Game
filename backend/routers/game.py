from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from database.database import get_db
from database.models import GameStateDB
from game_engine.game_session import GameSession

router = APIRouter(prefix="/game", tags=["game"])


# ──────────────────────────────────────────
# Request / Response schemas
# ──────────────────────────────────────────

class NewGameRequest(BaseModel):
    player_name: str


class CommandRequest(BaseModel):
    command: str


class GameResponse(BaseModel):
    session_id: str
    messages: list[str]
    state: dict


class AchievementsResponse(BaseModel):
    achievements: list[dict]


# ──────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────

def _load_session(session_id: str, db: Session) -> tuple[GameStateDB, GameSession]:
    record = db.query(GameStateDB).filter(GameStateDB.id == session_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Game session not found.")
    gs = GameSession.from_dict(record.get_session_data())
    return record, gs


def _save_session(record: GameStateDB, gs: GameSession, db: Session):
    data = gs.to_dict()
    record.set_session_data(data)
    record.command_count = gs.command_count
    record.game_over = gs.ending or ""
    db.commit()


# ──────────────────────────────────────────
# Routes
# ──────────────────────────────────────────

@router.post("/new", response_model=GameResponse)
def new_game(req: NewGameRequest, db: Session = Depends(get_db)):
    """Create a new game session for a player."""
    name = req.player_name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Player name cannot be empty.")

    gs = GameSession(player_name=name)
    intro = gs.get_intro()

    record = GameStateDB(
        player_name=name,
        session_data="{}",
    )
    record.set_session_data(gs.to_dict())
    db.add(record)
    db.commit()
    db.refresh(record)

    return GameResponse(
        session_id=str(record.id),
        messages=intro["messages"],
        state=intro["state"],
    )


@router.get("/{session_id}", response_model=GameResponse)
def load_game(session_id: str, db: Session = Depends(get_db)):
    """Load an existing game session and get current state."""
    record, gs = _load_session(session_id, db)
    state = gs.get_state()
    room = gs.world.get_room(gs.player.current_room)
    look_result = gs._describe_room(room, full=True)
    return GameResponse(
        session_id=session_id,
        messages=[f"Game loaded. Welcome back, {gs.player.name}!"] + look_result,
        state=state,
    )


@router.post("/{session_id}/command", response_model=GameResponse)
def send_command(session_id: str, req: CommandRequest, db: Session = Depends(get_db)):
    """Process a player command and return the result."""
    record, gs = _load_session(session_id, db)

    result = gs.process_command(req.command)
    _save_session(record, gs, db)

    return GameResponse(
        session_id=session_id,
        messages=result["messages"],
        state=result["state"],
    )


@router.get("/{session_id}/achievements", response_model=AchievementsResponse)
def get_achievements(session_id: str, db: Session = Depends(get_db)):
    """Get the achievement list for a session."""
    record, gs = _load_session(session_id, db)
    return AchievementsResponse(achievements=gs.world.achievements)


@router.delete("/{session_id}")
def delete_game(session_id: str, db: Session = Depends(get_db)):
    """Delete a game session."""
    record = db.query(GameStateDB).filter(GameStateDB.id == session_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Session not found.")
    db.delete(record)
    db.commit()
    return {"detail": "Session deleted."}
