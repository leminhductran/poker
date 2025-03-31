from flask import Flask, request, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from app.game.game import GameState  # Make sure this points to your Game class

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = {}

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    print(f"Client connected: {request.sid}")

@socketio.on("create_room")
def create_room(data):
    room_id = data.get("room_id")
    if room_id in rooms:
        emit("error", {"message": "Room already exists"})
        return
    rooms[room_id] = GameState()
    join_room(room_id)
    emit("room_created", {"room_id": room_id})

@socketio.on("join_room")
def join_room_handler(data):
    room_id = data.get("room_id")
    player_name = data.get("player_name")
    game = rooms.get(room_id)
    if game is None:
        emit("error", {"message": "Room not found"})
        return
    if len(game.players) >= 6:
        emit("error", {"message": "Room full"})
        return
    game.add_player(request.sid, {
        "name": player_name,
        "chips": 1000,
        "hand": [],
        "status": "active",
        "folded": False,
        "bet": 0
    })
    join_room(room_id)
    emit("player_joined", {"player_id": request.sid, "player_name": player_name}, room=room_id)

@socketio.on("start_game")
def start_game(data):
    room_id = data.get("room_id")
    game = rooms.get(room_id)
    if game:
        game.start_new_hand()
        emit("game_started", {
            "community_cards": game.community_cards,
            "pot": game.pot,
            "dealer_sid": game.dealer_sid,
            "current_turn": game.current_turn,
            "players": {
                sid: {
                    "name": p["name"],
                    "chips": p["chips"],
                    "bet": p["bet"]
                } for sid, p in game.players.items()
            }
        }, room=room_id)


@socketio.on("showdown")
def handle_showdown(data):
    room_id = data.get("room_id")
    game = rooms.get(room_id)
    if game:
        result = game.showdown()
        emit("showdown_result", result, room=room_id)

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
