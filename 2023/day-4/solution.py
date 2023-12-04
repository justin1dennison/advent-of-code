import re
import math
def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def parse_line(line: str) -> tuple[set[int], set[int]]:
    pattern = re.compile(r"\d+")
    card, numbers = line.split(":")
    winning_raw, your_raw = numbers.split("|")
    return set(int(n.group()) for n in pattern.finditer(winning_raw)), set(int(n.group()) for n in pattern.finditer(your_raw))


def one(data) -> int:
    total = 0
    for line in str.splitlines(data):
        winning, your = parse_line(line)
        results = winning.intersection(your)
        score = math.floor(2**(len(results) - 1))
        total += score
    return total


if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert one(sample_data) == 13
    print(f"{one(data)=}")
