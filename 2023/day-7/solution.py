from collections import Counter
from functools import cmp_to_key
from dataclasses import dataclass
from enum import Enum, auto


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


class Play(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    def __lt__(self, other: "Play"):
        return self.value < other.value


@dataclass
class Hand:
    cards: list[str]
    bid: int

    @classmethod
    def from_line(cls, line: str) -> "Hand":
        cards, bid = line.split(" ")
        return cls(cards=list(cards), bid=int(bid))

    def play(self) -> Play:
        counts = Counter(self.cards)
        groups = counts.most_common(n=2)
        if len(groups) == 1:
            return Play.FIVE_OF_A_KIND
        (_, n), (_, k), *_ = groups
        if n == 4:
            return Play.FOUR_OF_A_KIND
        if n == 3 and k == 2:
            return Play.FULL_HOUSE
        if n == 3 and k == 1:
            return Play.THREE_OF_A_KIND
        if n == 2 and k == 2:
            return Play.TWO_PAIR
        if n == 2 and k == 1:
            return Play.ONE_PAIR
        return Play.HIGH_CARD

    def __lt__(self, other: "Hand") -> bool:
        card_ranks = {card: value for value, card in enumerate("23456789TJQKA", start=1)}
        for left, right in zip(self.cards, other.cards):
            if left != right:
                return (self.play(), card_ranks[left]) < (other.play(), card_ranks[right])



def one(data: str) -> int:
    lines = [l for l in str.splitlines(data) if l]
    hands = [Hand.from_line(line) for line in lines]
    ranks = [(rank, hand) for rank, hand in enumerate(sorted(hands), start=1)]
    return sum(rank * hand.bid for rank, hand in ranks)


def two(data: str) -> int:
    ...


if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert one(sample_data) == 6440, f"{one(sample_data)=}"
    print(f"{one(data)=}")
    assert two(sample_data) == 0, f"{two(sample_data)=}"
    print(f"{two(data)=}")
