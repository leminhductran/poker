import random
from hand_evaluator import evaluate_best_hand

class Game:
    def __init__(self):
        self.players = {}
        self.dealer_sid = None
        self.small_blind = 10
        self.big_blind = 20
        self.pot = 0
        self.community_cards = []
        self.current_bet = 0
        self.stage = "waiting"
        self.current_turn = None
        self.deck = []
        self.round_bets = {}
        self.active_sids = []

    def add_player(self, sid, player_data):
        self.players[sid] = player_data
        self.active_sids.append(sid)

    def reset_deck(self):
        suits = ["♠", "♥", "♦", "♣"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = [rank + suit for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal_hole_cards(self):
        for sid in self.players:
            self.players[sid]["hand"] = [self.deck.pop(), self.deck.pop()]

    def deal_community_cards(self, count):
        if count == 3:
            self.community_cards += [self.deck.pop() for _ in range(3)]
        elif count == 1:
            self.community_cards.append(self.deck.pop())

    def start_new_hand(self):
        self.reset_deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.round_bets = {}
        self.stage = "pre-flop"
        for sid in self.players:
            self.players[sid].update({"status": "active", "bet": 0, "folded": False})
        self.deal_hole_cards()
        self.set_dealer()
        self.set_blinds()

    def set_dealer(self):
        if not self.dealer_sid or self.dealer_sid not in self.active_sids:
            self.dealer_sid = random.choice(self.active_sids)
        else:
            index = self.active_sids.index(self.dealer_sid)
            self.dealer_sid = self.active_sids[(index + 1) % len(self.active_sids)]

    def set_blinds(self):
        dealer_index = self.active_sids.index(self.dealer_sid)
        sb_index = (dealer_index + 1) % len(self.active_sids)
        bb_index = (dealer_index + 2) % len(self.active_sids)
        sb_sid = self.active_sids[sb_index]
        bb_sid = self.active_sids[bb_index]
        self.players[sb_sid]["chips"] -= self.small_blind
        self.players[sb_sid]["bet"] = self.small_blind
        self.players[bb_sid]["chips"] -= self.big_blind
        self.players[bb_sid]["bet"] = self.big_blind
        self.pot += self.small_blind + self.big_blind
        self.current_bet = self.big_blind
        self.current_turn = self.active_sids[(bb_index + 1) % len(self.active_sids)]


    def evaluate_all_hands(self):
        results = {}
        for sid, player in self.players.items():
            if not player.get("folded", False):
                rank, best_hand = evaluate_best_hand(player["hand"], self.community_cards)
                results[sid] = {
                    "name": player["name"],
                    "rank": rank,
                    "hand": best_hand
                }
        return results

    def get_winners(self):
        hands = self.evaluate_all_hands()
        if not hands:
            return [], None  # everyone folded

        best_rank = max(h["rank"] for h in hands.values())
        winners = [sid for sid, h in hands.items() if h["rank"] == best_rank]
        return winners, best_rank

    def showdown(self):
        winners, rank = self.get_winners()
        player_hands = {
            sid: {
                "hand": self.players[sid]["hand"],
                "name": self.players[sid]["name"]
            } for sid in self.players if not self.players[sid].get("folded", False)
        }
        return {
            "winners": winners,
            "rank": rank,
            "community_cards": self.community_cards,
            "player_hands": player_hands
        }
