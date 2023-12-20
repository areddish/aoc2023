from collections import defaultdict
from copy import copy, deepcopy
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
workflows = {}

def eval_workflow(part, workflows, workflow_name):
    for p in part.split(","):
        exec(p)

    while workflow_name not in ["R","A"]:
        for wf in workflows[workflow_name]:
            wf_parts = wf.split(":")
            if len(wf_parts) == 1:
                workflow_name = wf_parts[0]
                break
            rule, dest = wf_parts
            if eval(rule):
                workflow_name = dest
                break

    ans = [0,0,0,0]
    if workflow_name == "A":
        #print("ACCEPT")
        ans = []
        for single_part_def in part.split(","):
            ans.append(int(single_part_def.split("=")[1]))
        #assert len(ans) == 4
    #else:
        #print("REJECT")

    return ans

registers = []

#with open("test.txt") as file:
with open("day19.txt") as file:
    parse = True
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        if not line:
            parse = False
            continue
        if parse:
            parts = line.split("{")
            name, workflow = parts
            rules = workflow[:-1].split(",")
            workflows[name] = rules
            print (name,workflow)
        else:
            registers.append(line[1:-1])

    for reg in registers:
        x,m,a,s = eval_workflow(reg, workflows, "in")
        part1 += x+m+a+s
answer (part1)

#### Part 2

start = "in"
MIN = 1
MAX = 4000
# 1 < x < 4000
vals = {ch:[MIN, MAX] for ch in "xmas"}

# Update the range of numbers based on the operation.
# optional arg to negate the expression and do the
# opposite for the case where we are continuing past
# an approval branch.
#       greater_than_val < VAL < less_than_val
def update_range(op, val, range, negate=False):
    greater_than_val, less_than_val = range
    if not negate:
        if op == ">":
            greater_than_val = max(val+1, greater_than_val)
        else:
            assert op == "<"
            less_than_val = min(val-1, less_than_val)
    else:
        if op == ">":
            # behave like <=
            less_than_val = min(val, less_than_val)
        else:
            assert op == "<"
            # behave like >=
            greater_than_val = max(val, greater_than_val)
    return [greater_than_val, less_than_val]

def ranges_product(vals):
    ans = 1
    for k in vals:
        gt = vals[k][0]
        lt = vals[k][1]
        assert gt <= lt, f"{gt} < val < {lt}"
        ans *= (lt-gt) + 1
    return ans

def get_approve_count(workflows, register_values, workflow_name):
    # Rejected, nothing to contribute
    if workflow_name == "R":
        return 0
    
    # Accepted! Calculate the product
    if workflow_name == "A":
        return ranges_product(register_values)
    
    # This is the default destination, remove it to make processing
    # easier, we always take this for the left over ranges.
    default_dest = workflows[workflow_name][-1]

    # We'll try each of these rules and count approvals
    rules_to_try = workflows[workflow_name][:-1]
    ans = 0
    for rules in rules_to_try:
        # if the rule has a condition, apply it
        expr,dest = rules.split(":")
        register_name = expr[0]
        op = expr[1]
        val = int(expr[2:])

        # Positive acceptance path for rule
        update = update_range(op, val, register_values[register_name], negate=False)
        if update[1] >= update[0]:
            # Only update if accepted, and make a copy to not corrupt
            # the rest of the chain.
            copy_vals = deepcopy(register_values)
            copy_vals[register_name] = update
            ans += get_approve_count(workflows, copy_vals, dest)

        # otherwise, negate the rules as if we didn't take the positive path and
        # continue to test against the rules
        update = update_range(op, val, register_values[register_name], negate=True)
        if update[1] >= update[0]:
            register_values = deepcopy(register_values)
            # Only update if valid
            register_values[register_name] = update
        else:
            # we consumed the ranges or cannot continue
            break
    
    # This is the fallthrough default case, we need to account for it.
    return ans + get_approve_count(workflows, register_values, default_dest)

answer(get_approve_count(workflows, vals, "in"))
exit()
