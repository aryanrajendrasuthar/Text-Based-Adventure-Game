import json
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base


class GameStateDB(Base):
    __tablename__ = "game_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_name = Column(String(100), nullable=False)
    session_data = Column(Text, nullable=False)  # full JSON blob
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    command_count = Column(Integer, default=0)
    game_over = Column(String(20), default="")  # ending type or empty

    def set_session_data(self, data: dict):
        self.session_data = json.dumps(data)

    def get_session_data(self) -> dict:
        return json.loads(self.session_data)
