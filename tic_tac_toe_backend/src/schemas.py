from typing import List, Optional
from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int

    class Config:
        from_attributes = True

class GameBase(BaseModel):
    player1_id: int
    player2_id: Optional[int] = None

class GameCreate(GameBase):
    pass

class GameMove(BaseModel):
    row: int
    col: int

class GameState(BaseModel):
    id: int
    board: List[List[Optional[str]]]
    current_player: int
    is_completed: bool
    winner_id: Optional[int] = None
    is_draw: bool
    player1: Player
    player2: Optional[Player] = None

    class Config:
        from_attributes = True
