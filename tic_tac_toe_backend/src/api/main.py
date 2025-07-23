from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from src.database import engine, get_db
from src import models, schemas
from src.game_logic import TicTacToeGame

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tic Tac Toe API",
    description="API for playing Tic Tac Toe game",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "healthy"}

@app.post("/players/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """
    Create a new player
    """
    db_player = models.Player(name=player.name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@app.get("/players/", response_model=List[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    """
    Get all players
    """
    return db.query(models.Player).all()

@app.post("/games/", response_model=schemas.GameState)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    """
    Create a new game
    """
    player1 = db.query(models.Player).filter(models.Player.id == game.player1_id).first()
    if not player1:
        raise HTTPException(status_code=404, detail="Player 1 not found")

    if game.player2_id:
        player2 = db.query(models.Player).filter(models.Player.id == game.player2_id).first()
        if not player2:
            raise HTTPException(status_code=404, detail="Player 2 not found")

    db_game = models.Game(
        player1_id=game.player1_id,
        player2_id=game.player2_id,
        board=TicTacToeGame.create_empty_board(),
        current_player=1,
        is_completed=False
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@app.get("/games/{game_id}", response_model=schemas.GameState)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """
    Get game state by ID
    """
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.post("/games/{game_id}/move", response_model=schemas.GameState)
def make_move(game_id: int, move: schemas.GameMove, db: Session = Depends(get_db)):
    """
    Make a move in the game
    """
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.is_completed:
        raise HTTPException(status_code=400, detail="Game is already completed")

    if not TicTacToeGame.make_move(game.board, move.row, move.col, game.current_player):
        raise HTTPException(status_code=400, detail="Invalid move")

    # Check game status
    is_completed, winner_symbol, is_draw = TicTacToeGame.get_game_status(game.board)
    
    if is_completed:
        game.is_completed = True
        game.is_draw = is_draw
        if winner_symbol:
            game.winner_id = game.player1_id if winner_symbol == 'X' else game.player2_id
    else:
        # Switch current player
        game.current_player = 3 - game.current_player  # Switches between 1 and 2

    db.commit()
    db.refresh(game)
    return game

@app.get("/games/", response_model=List[schemas.GameState])
def get_games(db: Session = Depends(get_db)):
    """
    Get all games
    """
    return db.query(models.Game).all()
