import re

sample_input = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

sample_input_part2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def one(data: str) -> int:
    total = 0
    lines = [line for line in str.splitlines(data) if line]
    for line in lines:
        digits = [d for d in line if str.isdigit(d)]
        calibration_value = digits[0] + digits[-1]
        total += int(calibration_value)
    return total


def two(data: str) -> int:
    def translate(line: str) -> str:
        return (
            line.replace("one", "o1e")
            .replace("two", "t2o")
            .replace("three", "th3ee")
            .replace("four", "fo4r")
            .replace("five", "fi5e")
            .replace("six", "s6x")
            .replace("seven", "se7en")
            .replace("eight", "ei8ght")
            .replace("nine", "ni9e")
        )

    total = 0
    lines = [line for line in str.splitlines(data) if line]
    for line in lines:
        digits = [d for d in translate(line) if str.isdigit(d)]
        calibration_value = digits[0] + digits[-1]
        total += int(calibration_value)
    return total


if __name__ == "__main__":
    assert one(sample_input) == 142
    data = read_data("./input.txt")
    print(f"{one(data)=}")
    assert two(sample_input_part2) == 281
    print(f"{two(data)=}")
