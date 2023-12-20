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

LOW = "low"
HIGH = "high"

part1 = 0
part2 = 0

import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

class FlipFlop:
    def __init__(self, name, outs):
        self.name = name[1:]
        self.out = outs
        self.state = False # off
    def pulse_in(self, from_, pulse):
        if pulse == HIGH:
            return []
        assert pulse == LOW
        if self.state:
            # turning off
            send_ = LOW
        else:
            send_ = HIGH
        self.state = not self.state

        signals_to_send = []
        for dest in self.out:
            signals_to_send.append((dest, send_, self.name))
        return signals_to_send

class Conjunction:
    def __init__(self, name, outs):
        self.name = name[1:]
        self.out = outs
        self.memory = defaultdict(lambda: LOW)
        self.inputs = []

    def add_input(self, name):
        self.inputs.append(name)

    def pulse_in(self, from_, pulse):
        self.memory[from_] = pulse
        send_ = HIGH
        if all([self.memory[n] == HIGH for n in self.inputs]):
            send_ = LOW
        signals_to_send = []
        for dest in self.out:
            signals_to_send.append((dest, send_, self.name))
        return signals_to_send

        # for dest in self.out:
        #     dest.pulse_in(self, send_)

class Broadcaster:
    def __init__(self, outs):
        self.name = "broadcaster"
        self.out = outs
    
graph = {}
nodes = {}

def get_or_create_node(name, outs):
    global nodes
    if name in nodes:
        return nodes[name]
    
    node = None
    if name[0] == "%":
        node = FlipFlop(name, outs)
    elif name[0] == "&":
        node = Conjunction(name, outs)
    else:
        assert name == "broadcaster"
        node = Broadcaster(outs)

    return node

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day20.txt") as file:
    parse = True
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        src,dest = line.split(" -> ")
        # (dest, state)
        node = get_or_create_node(src, [x.strip() for x in dest.split(",")])
        nodes[node.name] = node

    # hook up inputs
    for node_name in nodes:
        n = nodes[node_name]
        if isinstance(n, Conjunction):
            for other_node_name in nodes:
                nn = nodes[other_node_name]
                if n.name in nn.out:
                    n.add_input(nn.name)
count = {
    LOW: 0,
    HIGH: 0
}        

# part 2 look for cycles. we want to know when rx is LOW, and since it's fed
# by the conjunction lv, we need to know when all of lv's inputs are high. So 
# look for cycles and use LCM to figure out when the individual inputs will all be high, 
# which will cause lv to output a low to rx!
cycles = {name: [] for name in nodes["lv"].inputs}

button_press = 0
while True:
    signals = []

    # account for button press
    count[LOW] += 1
    for dest in nodes["broadcaster"].out:
        signals.append((dest, LOW, "broadcaster"))

    # cycle through the signals        
    while signals:
        dest, send_, from_ = signals.pop(0)   
        count[send_] += 1
        #print(f"{from_} --{'LOW' if send_ == LOW else 'HIGH'}-> {dest}")

        if from_ in nodes["lv"].inputs and send_ == HIGH:
            cycles[from_].append(button_press)
            if len(cycles[from_]) > 2:
                cycles[from_].pop(0)
                #print(" ====== ")
                #for f in nodes["lv"].inputs:
                #    print (cycles[f][1] - cycles[f][0])
                if all([len(cycles[input_name]) == 2 for input_name in nodes["lv"].inputs]):
                    part2 = 1
                    for k in cycles:
                        part2 = lcm(part2, cycles[k][1]-cycles[k][0])
                    answer(part2)
                    exit()
        if dest in nodes:
            for generated_signal in nodes[dest].pulse_in(from_, send_):
                signals.append(generated_signal)
    button_press += 1
    if button_press == 1000:
        #print(f"LOW = {count[LOW]}, HIGH = {count[HIGH]}, {count[LOW]*count[HIGH]}")
        answer(count[LOW]*count[HIGH])