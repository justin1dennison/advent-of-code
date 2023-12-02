import re


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def parse_line(line: str) -> tuple[str, list[tuple[str, str]]]:
    round_pattern = re.compile(r"(?P<n>\d+)\s+(?P<color>\w+)")
    game_pattern = re.compile(r"Game\s+(?P<game_id>\d+)")
    game, rounds_raw = line.split(":")
    game_id = int(game_pattern.search(game).groupdict()["game_id"])
    rounds = [round_pattern.findall(r) for r in rounds_raw.split(";")]
    draws = [dict((color, int(n)) for n, color in r) for r in rounds]
    return game_id, draws


def one(data) -> int:
    limits = {"red": 12, "green": 13, "blue": 14}
    games = [parse_line(line) for line in data.splitlines() if line]
    game_ids = []
    for game_id, draws in games:
        if all(draw[color] <= limits[color]  
               for draw in draws
               for color in draw):
            game_ids.append(game_id) 
    return sum(game_ids)

def two(data) -> int:
    def power_of(game: tuple[int, list[tuple[str, int]]]) -> int:
        game_id, draws = game
        reds = max(d.get("red", 0) for d in draws)
        blues = max(d.get("blue", 0) for d in draws)
        greens = max(d.get("green", 0) for d in draws)
        return reds * blues * greens 

    games = [parse_line(line) for line in data.splitlines() if line]
    return sum(power_of(game)  for game in games)


if __name__ == "__main__":
    data = read_data("./input.txt")
    assert one(read_data("./sample-part1.txt")) == 8, "Part 1 Sample Data"
    print(one(data))
    assert two(read_data("./sample-part1.txt")) == 2286, "Part 2 Sample Data"
    print(two(data))
    
