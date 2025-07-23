from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    games_as_player1 = relationship("Game", foreign_keys="Game.player1_id", back_populates="player1")
    games_as_player2 = relationship("Game", foreign_keys="Game.player2_id", back_populates="player2")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=True)  # Nullable for single-player games
    board = Column(JSON)  # Store the game board as JSON
    current_player = Column(Integer)  # 1 or 2 to indicate whose turn it is
    is_completed = Column(Boolean, default=False)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    is_draw = Column(Boolean, default=False)

    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="games_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="games_as_player2")
