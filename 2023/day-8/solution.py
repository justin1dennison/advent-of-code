from itertools import cycle
import re

def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()

def parse_mapping(mapping: str) -> dict[str, tuple[str, str]]:
    pattern = re.compile(r"(?P<key>[A-Z]+)\s+=\s+\((?P<L>[A-Z]+),\s+(?P<R>[A-Z]+)\)")
    results = {}
    for m in pattern.finditer(mapping):
        group = m.groupdict()
        key = group.pop("key")
        results[key] = group
    return results


def one(data: str) -> int:
    instructions, mapping = data.split("\n\n")
    instructions = cycle(instructions)
    mapping = parse_mapping(mapping)
    count = 0 
    x = "AAA"
    for instruction in instructions:
        x = mapping.get(x).get(instruction)
        count += 1
        if x == "ZZZ":
            break
    return count


def two(data: str) -> int:
    ...



if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert one(sample_data) == 2, f"{one(sample_data)=}"
    print(f"{one(data)=}")
    assert two(sample_data) == 6, f"{two(sample_data)=}"
    print(f"{two(data)=}")
