from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property
from typing import Any


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


class Tile(StrEnum):
    GROUND = "."
    VERTICAL = "|"
    HORIZONTAL = "-"
    NE_BEND = "L"
    NW_BEND = "J"
    SW_BEND = "7"
    SE_BEND = "F"
    STARTING = "S"


@dataclass
class Grid:
    _grid: list[list[Any]]

    @classmethod
    def create(cls, data: str) -> "Grid":
        lines = (line for line in str.splitlines(data) if line)
        return cls(_grid=[[Tile(t) for t in list(line)] for line in lines])

    @classmethod
    def empty(cls, length: int, width: int) -> "Grid":
        _grid = [[None] * width] * length
        return cls(_grid=_grid)

    @property
    def starting_position(self) -> tuple[int, int]:
        for i, row in enumerate(self._grid):
            for j, val in enumerate(row):
                if val == Tile.STARTING:
                    return i, j

    @property
    def map(self) -> str:
        return "\n".join("".join(row) for row in self._grid)

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._grid), len(self._grid[0])


def distances(grid) -> "Grid":
    x, y = grid.starting_position
    nrows, ncols = grid.shape
    empty = Grid.empty(nrows, ncols)

    i, j = x, y
    while i>= 0 or j>= 0:
        


def one(data: str) -> int:
    grid = Grid.create(data)
    ds = distances(grid)


def two(data: str) -> int:
    ...


if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    sample_data_2 = read_data("./sample-2.txt")
    assert (one_result := one(sample_data)) == 4, f"{one_result=}"
    assert (one_result_2 := one(sample_data_2)) == 8, f"{one_result_2=}"
    print(f"{one(data)=}")
    assert (two_result := two(sample_data)) == 2, f"{two_result=}"
    print(f"{two(data)=}")
