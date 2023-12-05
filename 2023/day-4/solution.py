import math
import re
from dataclasses import dataclass, field
from typing import Callable


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


@dataclass
class Card:
    id: int
    winning: set[int]
    your: set[int]
    count: int = field(default=1)

    @classmethod
    def from_line(cls, line: str) -> "Card":
        pattern = re.compile(r"\d+")
        id_pattern = re.compile(r"Card\s+(?P<id>\d+)")
        card, numbers = line.split(":")
        card_id = int(id_pattern.search(card).groupdict()["id"])
        winning_raw, your_raw = numbers.split("|")
        winning, your = set(int(n.group()) for n in pattern.finditer(winning_raw)), set(
            int(n.group()) for n in pattern.finditer(your_raw)
        )
        return cls(id=card_id, winning=winning, your=your)

    def score(self, score_fn: Callable[[list[str]], int]) -> int:
        return score_fn(self.winning.intersection(self.your))


def part_one_score_strategy(r: list[str]) -> int:
    return math.floor(2 ** (len(r) - 1))


def one(data: str) -> int:
    cards = [Card.from_line(line) for line in str.splitlines(data)]
    return sum(c.score(part_one_score_strategy) for c in cards)


def part_two_score_strategy(r: list[str]) -> int:
    return len(r)


def two(data: str) -> int:
    cards = [Card.from_line(line) for line in str.splitlines(data)]
    for card in cards:
        score = card.score(part_two_score_strategy)
        rewards = cards[card.id : card.id + score]
        for reward in rewards:
            reward.count += card.count
    return sum(c.count for c in cards)


if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert one(sample_data) == 13, f"{one(sample_data)=}"
    print(f"{one(data)=}")
    assert two(sample_data) == 30, f"{two(sample_data)=}"
    print(f"{two(data)=}")
