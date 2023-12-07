from collections import Counter

###
#   Submission helper, print the answer and copy it to the clipboard
#   to reduce the amount of times I have the answer and mistype it :).
###
import pyperclip
answer_part = 1
def answer(v):
    global answer_part
    pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2

# Used to convert from card to a sortable numeric value. The order is 
# strongest to weakest.
ORDER = list("AKQJT98765432")
ORDER_RANK = { ch: len(ORDER)-ORDER.index(ch) for ch in ORDER}

ORDER_WITH_JOKERS = list("AKQT98765432J")
ORDER_WITH_JOKERS_RANK = { ch: len(ORDER_WITH_JOKERS)-ORDER_WITH_JOKERS.index(ch) for ch in ORDER_WITH_JOKERS}

# Maps card buckets from counters to a rank/strength. Value doesn't matter just needs
# to be decreasing.
HAND_RANKS = {
    (5,): 5,
    (1,4): 4,
    (2,3): 3,
    (1,1,3): 2,
    (1,2,2): 1,
    (1,1,1,2): 0,
    (1,1,1,1,1): -1
}

def rank(hand, use_wildcard=False):
    card_counter = Counter(hand)
    bucket_sizes = sorted(card_counter.values())

    if use_wildcard and 1 <= card_counter["J"] < 5:
        # We have jokers so we need to remove them from the buckets and
        # greedily apply the jokers to the biggest bucket we can to give
        # us the best hand.
        bucket_sizes.remove(card_counter["J"])
        bucket_sizes[-1] += card_counter["J"]

    card_strengths_rank = ORDER_WITH_JOKERS_RANK if use_wildcard else ORDER_RANK
    return [HAND_RANKS[tuple(bucket_sizes)]] + [card_strengths_rank[card] for card in hand]

def score_hands(hands_with_bids):
    result = 0
    for i,hand in enumerate(sorted(hands_with_bids, key=lambda x:x[0], reverse=False)):
        result += (i+1) * hand[1]
    return result

#with open("test.txt") as file:
with open("day7.txt") as file:
    hands = []
    hands_with_wildcards = []
    for line in file.readlines():
        hand, bid = line.strip().split(" ")
        bid = int(bid)
        hands.append((rank(hand), bid))
        hands_with_wildcards.append((rank(hand, use_wildcard=True), bid))

    ## Part 1
    answer(score_hands(hands))
    ## Part 2
    answer(score_hands(hands_with_wildcards))