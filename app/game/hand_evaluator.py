# hand_evaluator.py
from collections import Counter
from itertools import combinations

RANK_NAMES = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
RANK_VALUES = {name: i for i, name in enumerate(RANK_NAMES, start=2)}

HAND_RANKS = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}

def evaluate_hands(cards):
    best_score = 0
    for combo in combinations(cards, 5):
        score = evaluate_five_card_hand(combo)
        if score > best_score:
            best_score = score
    return best_score

def evaluate_five_card_hand(hand):
    values = sorted([card.value for card in hand], reverse=True)
    suits = [card.suit for card in hand]

    value_counter = Counter(values)
    suit_counter = Counter(suits)

    flush = None
    for suit, count in suit_counter.items():
        if count >= 5:
            flush = suit
            break

    is_straight_result, top_straight = is_straight(values)

    if flush and is_straight_result:
        flush_cards = [card.value for card in hand if card.suit == flush]
        is_flush_straight, top_flush_straight = is_straight(sorted(flush_cards, reverse=True))
        if is_flush_straight:
            if top_flush_straight == 12:
                return HAND_RANKS["Royal Flush"] * 1_000_000
            return HAND_RANKS["Straight Flush"] * 1_000_000 + top_flush_straight

    if 4 in value_counter.values():
        quad = [v for v, c in value_counter.items() if c == 4][0]
        return HAND_RANKS["Four of a Kind"] * 1_000_000 + quad

    if 3 in value_counter.values() and 2 in value_counter.values():
        triple = [v for v, c in value_counter.items() if c == 3][0]
        pair = [v for v, c in value_counter.items() if c == 2][0]
        return HAND_RANKS["Full House"] * 1_000_000 + triple * 100 + pair

    if flush:
        flush_values = sorted([card.value for card in hand if card.suit == flush], reverse=True)
        return HAND_RANKS["Flush"] * 1_000_000 + sum(flush_values[:5])

    if is_straight_result:
        return HAND_RANKS["Straight"] * 1_000_000 + top_straight

    if 3 in value_counter.values():
        triple = [v for v, c in value_counter.items() if c == 3][0]
        return HAND_RANKS["Three of a Kind"] * 1_000_000 + triple

    pairs = [v for v, c in value_counter.items() if c == 2]
    if len(pairs) >= 2:
        top_two = sorted(pairs, reverse=True)[:2]
        return HAND_RANKS["Two Pair"] * 1_000_000 + top_two[0] * 100 + top_two[1]

    if len(pairs) == 1:
        return HAND_RANKS["One Pair"] * 1_000_000 + pairs[0]

    return HAND_RANKS["High Card"] * 1_000_000 + sum(values[:5])

def is_straight(values):
    unique = sorted(set(values), reverse=True)
    for i in range(len(unique) - 4):
        if unique[i] - unique[i + 4] == 4:
            return True, unique[i]
    if set([12, 0, 1, 2, 3]).issubset(set(values)):
        return True, 3
    return False, None

def get_hand_rank_name(score):
    for name, base in reversed(HAND_RANKS.items()):
        if score >= base * 1_000_000:
            return name
    return "Unknown"
