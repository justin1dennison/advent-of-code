import re
import math
from typing import Callable, Iterable
from dataclasses import dataclass, field


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def parse_card(line: str) -> tuple[set[int], set[int]]:
    pattern = re.compile(r"\d+")
    card, numbers = line.split(":")
    winning_raw, your_raw = numbers.split("|")
    return set(int(n.group()) for n in pattern.finditer(winning_raw)), set(
        int(n.group()) for n in pattern.finditer(your_raw)
    )


def score(card : str, score_fn: Callable[[Iterable[str]], int]) -> int:
    winning, your = parse_card(card)
    results = winning.intersection(your)
    return score_fn(results)


def one(data: str) -> int:
    total = 0
    for line in str.splitlines(data):
        total += score(line, lambda r: math.floor(2 ** (len(r) - 1)))
    return total

@dataclass
class Card:
    id: int
    winning: set[int]
    your: set[int]
    count: int = field(default=1) 

    @classmethod
    def from_line(cls, id: int, line: str) -> "Card":
        winning, your = parse_card(line)
        return cls(id=id, winning=winning, your=your)

    def score(self, score_fn: Callable[[Iterable[str]], int] = len) -> int:
        return score_fn(self.winning.intersection(self.your))


def two(data: str) -> int:
    cards = [Card.from_line(i, line) for i, line in enumerate(str.splitlines(data))]
    for card in cards:
        score = card.score()
        rewards = cards[card.id + 1: card.id + score + 1]
        for reward in rewards:
            reward.count += card.count
    return sum(c.count for c in cards)
    
             

if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert one(sample_data) == 13
    print(f"{one(data)=}")
    assert two(sample_data) == 30, f"{two(sample_data)=}"
    print(f"{two(data)=}")
