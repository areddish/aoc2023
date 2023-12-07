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

part1 = 0
part2 = 0

# Used to convert from card to a sortable numeric value. The order is 
# strongest to weakest.
ORDER = list("AKQJT98765432")
ORDER_WITH_JOKERS = list("AKQT98765432J")

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

#with open("test.txt") as file:
with open("day7.txt") as file:
    type_buckets = defaultdict(list)
    type_buckets_with_wildcard = defaultdict(list)
    for line in file.readlines():
        hand, bid = line.strip().split(" ")
        rank(hand,int(bid), type_buckets)
        rank(hand,int(bid), type_buckets_with_wildcard, use_wildcard=True)

    # Process in this order and prepend the hand values with the type value so that when we
    # sort the type is considered first, then the card strength
    type_bucket_key_order = ["five", "four", "full", "three", "twopair", "pair", "high"]
    type_bucket_values = range(len(type_bucket_key_order)+1,0,-1)

    ## Part 1
    hand_values = []
    ORDER_RANK = { ch: len(ORDER)-ORDER.index(ch) for ch in ORDER}
    for i in range(len(type_bucket_key_order)):
        for hand, bid in type_buckets[type_bucket_key_order[i]]:
            hand_values.append(([type_bucket_values[i]] + [ORDER_RANK[card] for card in hand], bid))

    for i,hand in enumerate(sorted(hand_values, key=lambda x:x[0], reverse=False)):
        part1 += (i+1) * hand[1]

    ## Part 2
    hand_values = []
    ORDER_RANK = { ch: len(ORDER_WITH_JOKERS)-ORDER_WITH_JOKERS.index(ch) for ch in ORDER_WITH_JOKERS}
    for i in range(len(type_bucket_key_order)):
        t = type_bucket_key_order[i]
        hands = type_buckets_with_wildcard[t]
        for hand, bid in hands:
            hand_values.append(([type_bucket_values[i]] + [ORDER_RANK[card] for card in hand], bid))

    for i,hand_bid in enumerate(sorted(hand_values, key=lambda x:x[0], reverse=False)):
            part2 += (i+1) * hand_bid[1]
answer(part1)
answer(part2)