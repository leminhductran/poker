import random

class Deck:
    def __init__(self):
        self.suits = ["♠", "♥", "♦", "♣"]
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = [f"{rank}{suit}" for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def draw(self, count=1):
        if count == 1:
            return self.cards.pop()
        return [self.cards.pop() for _ in range(count)]
