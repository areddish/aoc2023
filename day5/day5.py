from collections import defaultdict

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


class Interval:
    def __init__(self, start, length):
        self.start = start
        self.end = start + length - 1
        self.length = length
    
    #  0 no overlap
    #  1 other_interval inside this one
    #  2 other_interval contains this one
    #  3 other_interval starts in this one
    #  4 other_interval ends in this one
    def compare(self, other_interval):
        # condition 0, out of range
        #|xxxx|  |-----|  or |----|   |xxxx|
        if self.end < other_interval.start or self.start > other_interval.end:
            return 0, None
        # condition 1, other_interval contained inside self
        # |--|xxxx|--|
        if self.start <= other_interval.start and self.end >= other_interval.end:
            return 1, None
        # condition 2, self contained inside other_interval
        # |xx|---|x|                
        if other_interval.start <= self.start and other_interval.end >= self.end:
            return 2, None
        
        # condition 3, other_interval starts in this one
        # |---|xxxxxxx|
        if self.start <= other_interval.start <= self.end:
            return 3, other_interval.start
        # condition 4 
        # |xxxx|----|
        if self.start <= other_interval.end <= self.end:
            return 4, other_interval.end

        raise "What? This shouldn't happen."
    
seeds = []
maps = defaultdict(list)
map_name = None
#with open("test.txt") as file:
with open("day5.txt") as file:
    for card, line in enumerate(file.readlines()):
        line = line.strip()
        if not line:
            map_name = None
            continue
        if not seeds:
            parts = line.split(":")
            seeds = [int(x) for x in parts[1].strip().split()]
            print(seeds)
            continue

        if not map_name:
            map_name = line.split()[0]
            print(map_name)
        else:
            maps[map_name].append([int(x) for x in line.split()])

def map_through_value(mapping, source):
    for m in mapping:
        dest = m[0]
        src = m[1]
        rng = m[2]
        if src <= source < src + rng:
            return dest + source - src
    return source


def map_through_range(mapping, source, source_range):
    results = []
    test_intervals = [Interval(source, source_range)]
    while test_intervals:
        test_interval = test_intervals.pop()
        for m in mapping:
            rng = m[2]
            source_interval = Interval(m[1], rng)
            dest_interval = Interval(m[0], rng)

            add_if_not_processed = True
            cmp_result, pivot = test_interval.compare(source_interval)
            if cmp_result == 0:
                # no overlap, test against other mappings. If not processed we return the 1:1 mapping
                add_if_not_processed = False
                continue
            elif cmp_result == 1:
                # The contained interval is trasnformed
                # The overflow is added back to transform
                results.append([dest_interval.start, dest_interval.length])
                test_interval = Interval(test_interval.start, source_interval.start-test_interval.start)
                test_intervals.append(Interval(source_interval.end, test_interval.end - source_interval.end))     
            elif cmp_result == 2:
                # full transform
                offset = dest_interval.start + test_interval.start - source_interval.start
                results.append([offset, test_interval.length])
                test_interval = None
                break
            elif cmp_result == 3:
                # beginning needs to be re-tested, end is transformed
                offset = dest_interval.start
                results.append([offset, test_interval.end - source_interval.start])
                test_interval = Interval(test_interval.start, source_interval.start - test_interval.start)
            elif cmp_result == 4:
                # end needs to be re-tested, start is trasnformed
                offset = dest_interval.start + test_interval.start - source_interval.start
                results.append([offset, source_interval.end - test_interval.start])
                test_interval = Interval(source_interval.end, test_interval.end - source_interval.end)
        if test_interval and add_if_not_processed: #test_interval and test_interval.start != source and test_interval.length != source_range:
            test_intervals.append(test_interval)

    return results if len(results) > 0 else [[source, source_range]]

locations = []
order = [ "seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location" ]
for seed in seeds:
    result = seed
    for o in order:
        result = map_through_value(maps[o], result)
    locations.append(result)
answer(min(locations))

locations = []
for i in range(0, len(seeds), 2):
    seed_start = seeds[i]
    seed_length = seeds[i+1]
    print(f"Processing {seed_start} {seeds[i+1]}")
    results = [[seed_start, seed_length]]
    for o in order:
        next_results = []
        for seed_start, seed_length in results:
            results = map_through_range(maps[o], seed_start, seed_length)
            #print(o, results)
            for r in results:
                next_results.append(r)
        results = next_results  
    for r in results:
        locations.append(r[0])
answer(min(locations))