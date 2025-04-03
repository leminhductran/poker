# player.py

class Player:
    DEFAULT_CHIPS = 1000

    def __init__(self, name):
        self.name = name                      # Player's name
        self.chips = self.DEFAULT_CHIPS       # Starting chips
        self.hand = []                        # Two hole cards
        self.current_bet = 0                  # Current bet in the round
        self.total_bet = 0                    # Total bet in the hand
        self.folded = False                   # Whether the player folded
        self.all_in = False                   # Whether the player is all-in
        self.in_hand = True                   # Whether player is still in the hand
        self.has_acted = False                # Whether player has acted in this round

    def reset_for_new_hand(self):
        """
        Resets player status for a new hand.
        """
        self.hand = []
        self.current_bet = 0
        self.total_bet = 0
        self.folded = False
        self.all_in = False
        self.in_hand = True
        self.has_acted = False

    def fold(self):
        """
        Player folds the current hand.
        """
        self.folded = True
        self.in_hand = False

    def go_all_in(self):
        """
        Player goes all-in, betting all chips.
        """
        self.all_in = True
        all_in_amount = self.chips
        self.chips = 0
        self.current_bet += all_in_amount
        self.total_bet += all_in_amount
        return all_in_amount

    def bet(self, amount):
        """
        Player places a bet. Automatically goes all-in if amount exceeds chips.
        """
        if amount >= self.chips:
            return self.go_all_in()
        self.chips -= amount
        self.current_bet += amount
        self.total_bet += amount
        return amount

    def check(self):
        """
        Player checks (does nothing).
        """
        self.has_acted = True

    def call(self, amount_to_call):
        """
        Player calls the current bet amount.
        """
        call_amount = min(amount_to_call, self.chips)
        return self.bet(call_amount)

    def raise_bet(self, raise_amount):
        """
        Player raises by a specified amount.
        """
        return self.bet(raise_amount)

    def __repr__(self):
        return (f"Player({self.name}, chips={self.chips}, current_bet={self.current_bet}, "
                f"folded={self.folded}, all_in={self.all_in})")

    def is_active(self):
        """Returns True if the player is not folded or all-in."""
        return not self.folded and not self.all_in

    def to_dict(self, include_hand=False):
        """Return a dictionary representation of the player (for emitting via SocketIO)."""
        data = {
            'name': self.name,
            'chips': self.chips,
            'folded': self.folded,
            'all_in': self.all_in,
            'current_bet': self.current_bet
        }
        if include_hand:
            data['hand'] = [str(card) for card in self.hand]
        return data
