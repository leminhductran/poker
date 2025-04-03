# game.py
import random
from .player import Player
from .deck import Deck
from .hand_evaluator import evaluate_hands, get_hand_rank_name

class Game:
    SMALL_BLIND = 10
    BIG_BLIND = 20

    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.stage = 'pre-flop'
        self.dealer_index = 0
        self.current_player_index = 0
        self.small_blind_index = 0
        self.big_blind_index = 0

    def rotate_dealer(self):
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        self.small_blind_index = (self.dealer_index + 1) % len(self.players)
        self.big_blind_index = (self.dealer_index + 2) % len(self.players)
        self.current_player_index = (self.dealer_index + 3) % len(self.players)

    def post_blinds(self):
        sb_player = self.players[self.small_blind_index]
        bb_player = self.players[self.big_blind_index]
        sb_amount = sb_player.bet(self.SMALL_BLIND)
        bb_amount = bb_player.bet(self.BIG_BLIND)
        self.pot += sb_amount + bb_amount
        self.current_bet = self.BIG_BLIND

    def start_new_hand(self):
        self.rotate_dealer()
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.stage = 'pre-flop'
        for player in self.players:
            player.reset_for_new_hand()
            player.hand = self.deck.draw_multiple(2)
        self.post_blinds()

    def advance_stage(self):
        for player in self.players:
            player.current_bet = 0
            player.has_acted = False

        if self.stage == 'pre-flop':
            self.deck.draw()  # burn one
            self.community_cards += self.deck.draw_multiple(3)
            self.stage = 'flop'
        elif self.stage == 'flop':
            self.deck.draw()
            self.community_cards.append(self.deck.draw())
            self.stage = 'turn'
        elif self.stage == 'turn':
            self.deck.draw()
            self.community_cards.append(self.deck.draw())
            self.stage = 'river'
        elif self.stage == 'river':
            self.stage = 'showdown'

    def get_current_player(self):
        return self.players[self.current_player_index]

    def rotate_to_next_player(self):
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if not self.players[self.current_player_index].folded and not self.players[self.current_player_index].all_in:
                break

    def place_bet(self, player, amount):
        actual_bet = player.bet(amount)
        self.pot += actual_bet
        self.current_bet = max(self.current_bet, player.current_bet)

    def all_players_have_called(self):
        active = [p for p in self.players if not p.folded and not p.all_in]
        return all(p.current_bet == self.current_bet for p in active)

    def play_betting_round(self):
        starting_index = self.current_player_index
        players_to_act = [p for p in self.players if not p.folded and not p.all_in]

        while True:
            current_player = self.get_current_player()
            if current_player not in players_to_act:
                self.rotate_to_next_player()
                continue

            call_amount = self.current_bet - current_player.current_bet
            self.place_bet(current_player, call_amount)

            current_player.has_acted = True
            self.rotate_to_next_player()

            if self.all_players_have_called():
                break

    def showdown(self):
        active_players = [p for p in self.players if not p.folded]
        results = [(p, evaluate_hands(p.hand + self.community_cards)) for p in active_players]
        results.sort(key=lambda x: x[1], reverse=True)
        winners = [results[0][0]]
        best_score = results[0][1]
        for player, score in results[1:]:
            if score == best_score:
                winners.append(player)
            else:
                break
        split_pot = self.pot // len(winners)
        for winner in winners:
            winner.chips += split_pot
        for p, score in results:
            p.best_hand_name = get_hand_rank_name(score)
        return winners

    def play_full_hand(self):
        self.start_new_hand()
        self.play_betting_round()

        while self.stage != 'showdown':
            self.advance_stage()
            if self.stage != 'showdown':
                self.play_betting_round()

        return self.showdown()
