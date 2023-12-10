# tests

# Part 1 tests
part1_tests = [
    ("test.txt", 4),
    ("test3.txt", 8),
    ("day10.txt", 6947)
]

# Part 1 Tests
part2_tests = [
    ("test2.txt", 4),
    ("test4.txt", 8),
    ("test5.txt", 10),
    ("day10.txt", 273)
]

from day10 import run

for file, p1_answer in part1_tests:
    print(f"Testing Part 1: {file}... ", end="")
    p1, p2 = run(file)
    if p1 == p1_answer:
        print(" correct!")
    else:
        print(f" FAIL! (expected: {p1_answer}, actual: {p1})")

for file, p2_answer in part2_tests:
    print(f"Testing Part 2: {file}... ", end="")
    p1, p2 = run(file)
    if p2 == p2_answer:
        print(" correct!")
    else:
        print(f" FAIL! (expected: {p2_answer}, actual: {p2})")
