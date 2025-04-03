# server.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from game.game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

games = {}  # room_code -> Game instance

@app.route('/')
def index():
    return render_template('index.html')

def broadcast_player_list(room):
    player_names = [p.name for p in games[room].players]
    socketio.emit('player_list', {'players': player_names}, room=room)

@socketio.on('create_room')
def on_create(data):
    room = data['room']
    name = data['name']
    join_room(room)

    if room not in games:
        games[room] = Game([name])
    else:
        games[room].players.append(name)

    emit('room_joined', {'message': f"{name} created and joined room {room}"}, room=room)
    broadcast_player_list(room)

@socketio.on('join_room')
def on_join(data):
    room = data['room']
    name = data['name']
    join_room(room)

    if room in games:
        games[room].players.append(name)
        emit('room_joined', {'message': f"{name} joined room {room}"}, room=room)
        broadcast_player_list(room)
    else:
        emit('error', {'message': 'Room does not exist'})

@socketio.on('start_hand')
def start_hand(data):
    room = data['room']
    game = games.get(room)
    if not game:
        emit('error', {'message': 'Game not found'})
        return

    game.start_new_hand()
    current = game.get_current_player().name

    socketio.emit('hand_started', {
        'community_cards': [],
        'pot': game.pot,
        'current_turn': current,
        'players': [
            {
                'name': p.name,
                'hand': [str(card) for card in p.hand],
                'chips': p.chips,
                'folded': p.folded
            }
            for p in game.players
        ]
    }, room=room)

@socketio.on('player_action')
def on_action(data):
    room = data['room']
    name = data['name']
    action = data['action']  # 'fold', 'call', 'raise'
    amount = data.get('amount', 0)

    game = games.get(room)
    player = next(p for p in game.players if p.name == name)

    if action == 'fold':
        player.fold()
    elif action == 'call':
        to_call = game.current_bet - player.current_bet
        game.place_bet(player, to_call)
    elif action == 'raise':
        game.place_bet(player, amount)

    game.rotate_to_next_player()
    current = game.get_current_player().name

    if game.all_players_have_called():
        game.advance_stage()
        if game.stage == 'showdown':
            winners = game.showdown()
            socketio.emit('hand_result', {
                'community_cards': [str(card) for card in game.community_cards],
                'pot': game.pot,
                'players': [
                    {
                        'name': p.name,
                        'hand': [str(card) for card in p.hand],
                        'chips': p.chips,
                        'folded': p.folded,
                        'hand_rank': p.best_hand_name
                    } for p in game.players
                ],
                'winners': [w.name for w in winners]
            }, room=room)
            return

    socketio.emit('game_update', {
        'community_cards': [str(card) for card in game.community_cards],
        'pot': game.pot,
        'current_turn': current,
        'players': [
            {
                'name': p.name,
                'chips': p.chips,
                'folded': p.folded,
                'current_bet': p.current_bet
            } for p in game.players
        ]
    }, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)