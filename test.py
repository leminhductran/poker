from app.game.deck import Deck

deck = Deck()

print("🃏 Shuffled deck (52 cards):")
print(deck.cards)
print(f"Cards in deck: {len(deck)}")

print("\n🎯 Drawing 2 hole cards:")
hole_cards = deck.draw(2)
print("Hole cards:", hole_cards)
print(f"Cards left in deck: {len(deck)}")

print("\n🔥 Drawing the flop:")
flop = deck.draw(3)
print("Flop:", flop)

print("\n🌪 Drawing the turn:")
turn = deck.draw(1)
print("Turn:", turn)

print("\n💧 Drawing the river:")
river = deck.draw(1)
print("River:", river)

print(f"Cards left in deck: {len(deck)}")
