import random

class Card:
    def __init__(self, value, suit):
        self.value = value  # 0-12 (Two to Ace)
        self.suit = suit    # 0-3 (Diamonds, Clubs, Hearts, Spades)
        self.showing = True

    def __repr__(self):
        if not self.showing:
            return "[CARD]"

        value_names = [
            "Two", "Three", "Four", "Five", "Six", "Seven",
            "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"
        ]
        suit_names = ["Diamonds", "Clubs", "Hearts", "Spades"]

        return f"{value_names[self.value]} of {suit_names[self.suit]}"

class Deck(list):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        """Reset the deck to a full 52-card deck and shuffle it."""
        self.clear()
        suits = range(4)
        values = range(13)
        [[self.append(Card(value, suit)) for suit in suits] for value in values]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self)
        print("\n-- deck shuffled --")

    def draw(self):
        if not self:
            raise ValueError("Cannot draw from empty deck")
        return self.pop(0)

    def draw_multiple(self, count):
        if len(self) < count:
            raise ValueError("Not enough cards to draw")
        return [self.draw() for _ in range(count)]

    def burn(self):
        """Burn the top card (remove it from the deck without using)."""
        if not self:
            raise ValueError("Cannot burn from an empty deck")
        self.pop(0)

    def __repr__(self):
        return f"Standard deck of cards\n{len(self)} cards remaining"
