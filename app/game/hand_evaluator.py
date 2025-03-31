from itertools import combinations
from collections import Counter

def rank_value(card):
    rank_str = card[:-1]
    return {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 11, "Q": 12, "K": 13, "A": 14
    }[rank_str]

def suit_value(card):
    return card[-1]

def evaluate_5_card_hand(hand):
    ranks = [rank_value(c) for c in hand]
    suits = [suit_value(c) for c in hand]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    flush_suit = next((s for s, count in suit_counts.items() if count >= 5), None)
    flush_cards = [card for card in hand if suit_value(card) == flush_suit] if flush_suit else []

    sorted_unique = sorted(set(ranks), reverse=True)
    if 14 in sorted_unique:
        sorted_unique.append(1)
    straight_high = None
    for i in range(len(sorted_unique) - 4):
        window = sorted_unique[i:i+5]
        if window == list(range(window[0], window[0]-5, -1)):
            straight_high = window[0]
            break

    if flush_suit and len(flush_cards) >= 5:
        flush_ranks = sorted([rank_value(c) for c in flush_cards], reverse=True)
        if 14 in flush_ranks:
            flush_ranks.append(1)
        for i in range(len(flush_ranks) - 4):
            window = flush_ranks[i:i+5]
            if window == list(range(window[0], window[0]-5, -1)):
                if window[0] == 14:
                    return (10, [14])  
                return (9, [window[0]])  

    if 4 in rank_counts.values():
        four = [r for r in rank_counts if rank_counts[r] == 4][0]
        kicker = max(r for r in ranks if r != four)
        return (8, [four, kicker])

    trips = [r for r in rank_counts if rank_counts[r] == 3]
    pairs = [r for r in rank_counts if rank_counts[r] == 2]
    if trips:
        three = max(trips)
        if len(trips) > 1:
            pair = max([r for r in trips if r != three] + pairs)
        elif pairs:
            pair = max(pairs)
        else:
            pair = None
        if pair:
            return (7, [three, pair])

    if flush_suit:
        top_five = sorted([rank_value(c) for c in flush_cards], reverse=True)[:5]
        return (6, top_five)

    if straight_high:
        return (5, [straight_high])

    if trips:
        three = max(trips)
        kickers = sorted([r for r in ranks if r != three], reverse=True)[:2]
        return (4, [three] + kickers)
    
    if len(pairs) >= 2:
        top_two = sorted(pairs, reverse=True)[:2]
        kicker = max([r for r in ranks if r not in top_two])
        return (3, top_two + [kicker])

    if len(pairs) == 1:
        pair = pairs[0]
        kickers = sorted([r for r in ranks if r != pair], reverse=True)[:3]
        return (2, [pair] + kickers)

    return (1, sorted(ranks, reverse=True)[:5])

def evaluate_best_hand(player_hand, community_cards):
    all_7 = player_hand + community_cards
    best_rank = (0, [])
    best_hand = None
    for combo in combinations(all_7, 5):
        rank = evaluate_5_card_hand(combo)
        if rank > best_rank:
            best_rank = rank
            best_hand = combo
    return best_rank, best_hand
