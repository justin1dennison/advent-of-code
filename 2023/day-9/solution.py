from itertools import pairwise

type History = list[list[int]]


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def history(seq: list[int]) -> History:
    results = [seq]
    while sum(seq) != 0:
        seq = [y - x for x, y in pairwise(seq)]
        results.append(seq)
    return results


def next_value(history: History) -> int:
    return sum(xs[-1] + ys[-2] for xs, ys in pairwise(reversed(history)))


def beginning_value(history: History) -> int:
    last, *rest = list(reversed(history))
    ns = [0]
    for i, h in enumerate(rest):
        ns.append(h[0] - ns[i])
    return ns[-1]


def one(data: str) -> int:
    lines = [line for line in str.splitlines(data)]
    seqs = [[int(n) for n in line.split(" ") if n] for line in lines]
    return sum(next_value(history(seq)) for seq in seqs)


def two(data: str) -> int:
    lines = [line for line in str.splitlines(data)]
    seqs = [[int(n) for n in line.split(" ") if n] for line in lines]
    return sum(beginning_value(history(seq)) for seq in seqs)


if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert (one_result := one(sample_data)) == 114, f"{one_result=}"
    print(f"{one(data)=}")
    assert (two_result := two(sample_data)) == 2, f"{two_result=}"
    print(f"{two(data)=}")
