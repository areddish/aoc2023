from collections import defaultdict

# Every year I say I should look into networkx for these types of problems...
# Found minimum_cut which seemed to be referenced by "Cut" wires, and worked.
import networkx

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

nx_graph = networkx.Graph()
node_names = set()
#with open("test.txt") as file:
with open("day25.txt") as file:
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        # name: dest components / bidirectional
        components = line.split(" ")
        src = components[0][:-1]
        for c in components[1:]:
            node_names.add(src)
            node_names.add(c)
            nx_graph.add_edge(src, c, capacity=1)
            nx_graph.add_edge(c, src, capacity=1)

    node_names = list(node_names)
    e1 = node_names[0]
    for e2 in node_names[1:]:
        c, (group1, group2) = networkx.minimum_cut(nx_graph, e1, e2)
        if c == 3:
            answer(len(group1)*len(group2))
            exit() #break
