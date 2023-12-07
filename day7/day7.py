from collections import defaultdict, Counter

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
ORDER_WITH_JOKERS = list("AKQT98765432J")

# Process in this order and prepend the hand values with the type value so that when we
# sort the type is considered first, then the card strength
TYPE_BUCKET_KEY_ORDER = ["five", "four", "full", "three", "twopair", "pair", "high"]
TYPE_BUCKET_VALUES = range(len(TYPE_BUCKET_KEY_ORDER)+1,0,-1)

def rank(hand, bid, type, use_wildcard=False):
    card_counter = Counter(hand)
    joker_count = card_counter["J"] if use_wildcard else 0
    hand_type = None

    if len(card_counter) == 1:
        hand_type = "five"
    elif len(card_counter) == 5:
        if joker_count == 0:
            hand_type = "high"
        elif joker_count == 1: 
            hand_type = "pair"
        else:
            assert False, hand       
    elif len(card_counter) == 4:
        if joker_count == 0:
            hand_type = "pair"
        elif joker_count == 1 or joker_count == 2:  
            hand_type = "three"
        else:
            assert False, hand       
    elif len(card_counter) == 2:
        # four of a kind or full house. If most common is 3 then we know it's full house    
        if card_counter.most_common(1)[0][1] == 3:
            if joker_count == 0:            
                hand_type = "full"
            elif joker_count == 1:
                hand_type = "four"
            elif joker_count == 2 or joker_count == 3:
                hand_type = "five"
            else:
                assert False, hand       
        else:
            # four of a kind
            if joker_count == 0:                        
                hand_type = "four"
            elif joker_count == 1 or joker_count == 4:
                hand_type = "five"
            else:
                assert False, hand       
    elif len(card_counter) == 3:    
        # two pair or three of a kind. If the most common is 3 then we know its three of a kind
        if card_counter.most_common(1)[0][1] == 3:
            if joker_count == 0:            
                hand_type = "three"
            elif 1 <= joker_count <= 3:
                hand_type = "four"
            else:
                assert False, hand       
        else:
            # two pair
            if joker_count == 0: 
                hand_type = "twopair"
            elif joker_count == 1:
                hand_type = "full"
            elif joker_count == 2:
                hand_type = "four"
            else:
                assert False, hand
    else:
        assert False, hand

    type[hand_type].append((hand, bid))                

def score_hands(type_buckets, card_strengths):
    result = 0
    hand_values = []
    card_strengths_rank = { ch: len(card_strengths)-card_strengths.index(ch) for ch in card_strengths}
    for i in range(len(TYPE_BUCKET_KEY_ORDER)):
        for hand, bid in type_buckets[TYPE_BUCKET_KEY_ORDER[i]]:
            hand_values.append(([TYPE_BUCKET_VALUES[i]] + [card_strengths_rank[card] for card in hand], bid))

    for i,hand in enumerate(sorted(hand_values, key=lambda x:x[0], reverse=False)):
        result += (i+1) * hand[1]
    return result

#with open("test.txt") as file:
with open("day7.txt") as file:
    type_buckets = defaultdict(list)
    type_buckets_with_wildcard = defaultdict(list)
    for line in file.readlines():
        hand, bid = line.strip().split(" ")
        rank(hand,int(bid), type_buckets)
        rank(hand,int(bid), type_buckets_with_wildcard, use_wildcard=True)

    ## Part 1
    answer(score_hands(type_buckets, ORDER))
    ## Part 2
    answer(score_hands(type_buckets_with_wildcard, ORDER_WITH_JOKERS))