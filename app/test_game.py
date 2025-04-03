# test_game.py (now inside app/)
from game.game import Game


def main():
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    game = Game(player_names)

    winners = game.play_full_hand()

    print("\n=== Hand Result ===")
    print(f"Community cards: {[str(card) for card in game.community_cards]}")
    print(f"Pot: {game.pot}")
    print("\nPlayers:")
    for p in game.players:
        print(f"{p.name} | Hand: {[str(card) for card in p.hand]} | Chips: {p.chips} | Folded: {p.folded}")

    print("\nWinners:")
    for winner in winners:
        print(f"{winner.name} wins with hand {[str(card) for card in winner.hand]}")

if __name__ == "__main__":
    main()
