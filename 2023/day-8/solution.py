from itertools import cycle
import re
import math

def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()

def parse_mapping(mapping: str) -> dict[str, tuple[str, str]]:
    pattern = re.compile(r"(?P<key>[A-Z1-9]+)\s+=\s+\((?P<L>[A-Z1-9]+),\s+(?P<R>[A-Z1-9]+)\)")
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
    instructions, mapping = data.split("\n\n")
    mapping = parse_mapping(mapping)
    counts = []
    starts = [k for k in mapping.keys() if k.endswith("A")]
    for i, position in enumerate(starts):
        paths = cycle(instructions)
        count = 0
        while not position.endswith("Z"):
            path = next(paths)
            count += 1
            position = mapping[position][path]
        counts.append(count)

    return math.lcm(*counts)



if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    sample_data_two = read_data("./sample-2.txt")
    assert one(sample_data) == 2, f"{one(sample_data)=}"
    print(f"{one(data)=}")
    assert two(sample_data_two) == 6, f"{two(sample_data_two)=}"
    print(f"{two(data)=}")
