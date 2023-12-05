import re
from dataclasses import dataclass
from functools import partial
from itertools import islice, tee


def read_data(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


@dataclass
class MapEntry:
    source: int
    destination: int
    length: int

    def __contains__(self, value: int) -> bool:
        return self.source <= value <= self.source + self.length

    def translate(self, value: int) -> int:
        return self.destination + abs(self.source - value)

    def inverse_translate(self, value: int) -> int:
        return self.source + abs(self.destination - value)

    def in_destinations(self, value):
        return self.destination <= value <= self.destination + self.length


@dataclass
class Map:
    entries: list[MapEntry]

    @classmethod
    def from_section(cls, section: str) -> "Map":
        _, *lines = str.splitlines(section)
        entries = []
        for line in lines:
            destination, source, length = [int(i) for i in line.split(" ")]
            entries.append(
                MapEntry(source=source, destination=destination, length=length)
            )
        return cls(entries=entries)

    def __call__(self, value: int) -> int:
        for entry in self.entries:
            if value in entry:
                return entry.translate(value)
        return value

    def inverse(self, value: int) -> int:
        for entry in self.entries:
            if entry.in_destinations(value):
                return entry.inverse_translate(value)
        return value

    def destinations(self):
        for e in self.entries:
            for n in range(e.destination, e.destination + e.length):
                yield n


@dataclass
class SeedBank:
    ranges: list[range]

    @classmethod
    def from_section(cls, section: str) -> "SeedBank":
        one, two = tee((int(s) for s in section[len("seeds:") :].split(" ") if s), 2)
        starts = islice(one, 0, None, 2)
        lengths = islice(two, 1, None, 2)
        seed_ranges = [range(s, s + l) for s, l in zip(starts, lengths)]
        return cls(ranges=seed_ranges)

    def __iter__(self):
        for seed_range in self.ranges:
            for seed in seed_range:
                yield seed

    def __len__(self):
        return sum(len(r) for r in self.ranges)

    def __contains__(self, value):
        return any(value in r for r in self.ranges)


def apply(pipeline: list[Map], value: int) -> int:
    for fn in pipeline:
        value = fn(value)
    return value


def one(data: str) -> int:
    sections = data.split("\n\n")
    (
        seeds_data,
        seed_to_soil_map_data,
        soil_to_fertilizer_map_data,
        fertilizer_to_water_map_data,
        water_to_light_map_data,
        light_to_temperature_map_data,
        temperature_to_humidity_map_data,
        humidity_to_location_map_data,
    ) = sections
    seeds = [int(s) for s in seeds_data[len("seeds:") :].split(" ") if s]
    seed_to_soil_map = Map.from_section(seed_to_soil_map_data)
    soil_to_fertilizer_map = Map.from_section(soil_to_fertilizer_map_data)
    fertilizer_to_water_map = Map.from_section(fertilizer_to_water_map_data)
    water_to_light_map = Map.from_section(water_to_light_map_data)
    light_to_temperature_map = Map.from_section(light_to_temperature_map_data)
    temperature_to_humidity_map = Map.from_section(temperature_to_humidity_map_data)
    humidity_to_location_map = Map.from_section(humidity_to_location_map_data)
    pipeline = [
        seed_to_soil_map,
        soil_to_fertilizer_map,
        fertilizer_to_water_map,
        water_to_light_map,
        light_to_temperature_map,
        temperature_to_humidity_map,
        humidity_to_location_map,
    ]
    fn = partial(apply, pipeline)
    return min(fn(seed) for seed in seeds)


def two(data: str) -> int:
    sections = data.split("\n\n")
    (
        seeds_data,
        seed_to_soil_map_data,
        soil_to_fertilizer_map_data,
        fertilizer_to_water_map_data,
        water_to_light_map_data,
        light_to_temperature_map_data,
        temperature_to_humidity_map_data,
        humidity_to_location_map_data,
    ) = sections

    seeds = SeedBank.from_section(seeds_data)
    seed_to_soil_map = Map.from_section(seed_to_soil_map_data)
    soil_to_fertilizer_map = Map.from_section(soil_to_fertilizer_map_data)
    fertilizer_to_water_map = Map.from_section(fertilizer_to_water_map_data)
    water_to_light_map = Map.from_section(water_to_light_map_data)
    light_to_temperature_map = Map.from_section(light_to_temperature_map_data)
    temperature_to_humidity_map = Map.from_section(temperature_to_humidity_map_data)
    humidity_to_location_map = Map.from_section(humidity_to_location_map_data)
    pipeline = [
        seed_to_soil_map,
        soil_to_fertilizer_map,
        fertilizer_to_water_map,
        water_to_light_map,
        light_to_temperature_map,
        temperature_to_humidity_map,
        humidity_to_location_map,
    ]

    fn = partial(apply, reversed(pipeline))


if __name__ == "__main__":
    data = read_data("./input.txt")
    sample_data = read_data("./sample.txt")
    assert one(sample_data) == 35, f"{one(sample_data)=}"
    print(f"{one(data)=}")
    assert two(sample_data) == 46, f"{two(sample_data)=}"
    # print(f"{two(data)=}")
