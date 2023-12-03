import re
from dataclasses import dataclass
from pprint import pprint


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


@dataclass
class Symbol:
    value: str
    row: int
    position: int


@dataclass
class Number:
    row: int
    value: int
    start: int
    end: int

    def is_near(self, symbol: Symbol) -> bool:
        return (self.row - symbol.row in {-1, 0, 1}) and (self.start - 1 <= symbol.position <= self.end)


def one(data: str) -> int:
    numpattern = re.compile(r"(?P<number>\d+)")
    symbolpattern = re.compile(r"(?P<symbol>[%//*$+#@=&-])")
    numbers = []
    symbols = []
    for i, line in enumerate(str.splitlines(data)):
        num_matches = (
            (m.groupdict()["number"], m.span()) for m in numpattern.finditer(line)
        )
        for value, (start, end) in num_matches:
            numbers.append(Number(row=i, value=int(value), start=start, end=end))

        symbol_matches = (
            (m.groupdict()["symbol"], m.span()) for m in symbolpattern.finditer(line)
        )
        for value, (position, _) in symbol_matches:
            symbols.append(Symbol(row=i, value=value, position=position))
    return sum(n.value for n in numbers for s in symbols if n.is_near(s))


if __name__ == "__main__":
    data = read_data("./input.txt")
    one_sample = one(read_data("./sample1.txt"))
    assert one_sample == 4361, f"{one_sample=}"
    print(f"{one(data)=}")
