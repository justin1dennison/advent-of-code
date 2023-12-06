import re
from functools import reduce
from operator import mul


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def one(data: str) -> int:
    pattern = re.compile(r"\d+")
    lines = [l for l in str.splitlines(data) if l]
    times, distances = lines
    times = [int(f.group()) for f in pattern.finditer(times)]
    distances = [int(f.group()) for f in pattern.finditer(distances)]
    counts = [
        sum(
            1 if (acceleration * (time - acceleration) > distance) else 0
            for acceleration in range(1, time + 1)
        )
        for time, distance in zip(times, distances)
    ]
    return reduce(mul, counts)


def two(data: str) -> int:
    pattern = re.compile(r"\d+")
    lines = [l for l in str.splitlines(data) if l]
    times, distances = lines
    time = int(''.join(f.group() for f in pattern.finditer(times)))
    distance = int(''.join(f.group() for f in pattern.finditer(distances)))
    times = range(time)

    first = None
    for t in times:
        if t * (time - t) >= distance:
            first = t
            break
    last = None
    for t in reversed(times):
        if t * (time - t) >= distance:
            last = t
            break
    return last - first + 1


if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert one(sample_data) == 288, f"{one(sample_data)=}"
    print(f"{one(data)=}")
    assert two(sample_data) == 71503, f"{two(sample_data)=}"
    print(f"{two(data)=}")
