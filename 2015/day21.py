from dataclasses import dataclass
from typing import Optional, Tuple
import re
from itertools import combinations
from aocd import get_data

"""INVENTORY"""


@dataclass
class Item:
    name: str
    cost: int
    damage: int = 0
    armor: int = 0

    @property
    def type(self):
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.name} ({self.type}): Cost {self.cost}, Damage +{self.damage}, Armor +{self.armor}>"


class Weapon(Item):
    @property
    def type(self):
        return "Weapon"


class Armor(Item):
    @property
    def type(self):
        return "Armor"


class Ring(Item):
    @property
    def type(self):
        return "Ring"


ITEM_SHOP_DATA = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""


def parse_item_shop(data: str) -> dict:
    item_shop = {}
    sublists = [[i for i in sublist.split("\n")] for sublist in data.split("\n\n")]
    for sublist in sublists:
        for i, line in enumerate(sublist):
            if i == 0:
                item_type = re.findall(r"^\w+(?=:)", line)[0]
                item_shop[item_type] = []
            else:
                name, cost, damage, armor = re.split(r"\s\s+", line)
                cost = int(cost)
                damage = int(damage)
                armor = int(armor)
                if item_type == "Weapons":
                    item_shop[item_type].append(
                        Weapon(name=name, cost=cost, damage=damage, armor=armor)
                    )
                elif item_type == "Armor":
                    item_shop[item_type].append(
                        Armor(name=name, cost=cost, damage=damage, armor=armor)
                    )
                elif item_type == "Rings":
                    item_shop[item_type].append(
                        Ring(name=name, cost=cost, damage=damage, armor=armor)
                    )
    return item_shop


"""CHARACTERS"""


@dataclass
class Fighter:
    hit_points: int = 100
    base_damage: int = 0
    base_armor: int = 0
    name: Optional[str] = "Player"

    weapon: Optional[Weapon] = None
    armor: Optional[Armor] = None
    rings: Tuple[Ring] = ()  # errors out if you try to make this a list

    def __str__(self):
        return f"Fighter {self.name}"

    @property
    def attack_score(self) -> int:
        score = self.base_damage
        if self.weapon:
            score += self.weapon.damage
        if self.rings:
            score += sum([r.damage for r in self.rings])
        return score

    @property
    def armor_score(self) -> int:
        score = self.base_armor
        if self.armor:
            score += self.armor.armor
        if self.rings:
            score += sum([r.armor for r in self.rings])
        return score

    def damage_dealt(self, other) -> int:
        return max(1, self.attack_score - other.armor_score)

    @property
    def is_alive(self):
        return self.hit_points > 0

    @property
    def build_cost(self):
        cost = 0
        if self.weapon:
            cost += self.weapon.cost
        if self.armor:
            cost += self.armor.cost
        if self.rings:
            cost += sum([r.cost for r in self.rings])
        return cost


def parse_boss(data: str) -> Fighter:
    hit_points, damage, armor = re.findall(r"\d+", data)
    boss = Fighter(
        hit_points=int(hit_points),
        base_damage=int(damage),
        base_armor=int(armor),
        name="Boss",
    )
    return boss


def fight(player: Fighter, boss: Fighter) -> str:
    """Simulate a fight between a player character and the boss. Return the
    name of the winner."""
    is_player_turn = True
    while player.is_alive and boss.is_alive:
        # TODO: You don't have to simulate this explicitly; from damage/armor
        # scores alone we can know how many turns it will take for boss to kill
        # the player and vice versa. just see which is greater, tie goes to the player
        if is_player_turn:
            # Player attacks Boss
            boss.hit_points -= player.damage_dealt(boss)
            is_player_turn = False
        else:
            # Boss attacks player
            player.hit_points -= boss.damage_dealt(player)
            is_player_turn = True
    return boss.name if boss.is_alive else player.name


def part1(input: str):
    min_cost = float("inf")
    item_shop = parse_item_shop(ITEM_SHOP_DATA)
    for weapon in item_shop["Weapons"]:
        for armor in item_shop["Armor"]:
            for rings in combinations(item_shop["Rings"], 2):
                # You must use the weapon, may use the armor, can use either/both rings
                player_options = [
                    Fighter(weapon=weapon),
                    Fighter(weapon=weapon, rings=(rings[0],)),
                    Fighter(weapon=weapon, rings=(rings[1],)),
                    Fighter(weapon=weapon, rings=rings),
                    Fighter(weapon=weapon, armor=armor),
                    Fighter(weapon=weapon, armor=armor, rings=(rings[0],)),
                    Fighter(weapon=weapon, armor=armor, rings=(rings[1],)),
                    Fighter(weapon=weapon, armor=armor, rings=rings),
                ]
                for player in player_options:
                    boss = parse_boss(input)
                    winner = fight(player, boss)
                    if winner == "Player" and player.build_cost < min_cost:
                        min_cost = player.build_cost
    print(f"Part 1 answer: {min_cost}")
    return min_cost


def part2(input: str):
    max_cost = 0
    item_shop = parse_item_shop(ITEM_SHOP_DATA)
    for weapon in item_shop["Weapons"]:
        for armor in item_shop["Armor"]:
            for rings in combinations(item_shop["Rings"], 2):
                # You must use the weapon, may use the armor, can use either/both rings
                player_options = [
                    Fighter(weapon=weapon),
                    Fighter(weapon=weapon, rings=(rings[0],)),
                    Fighter(weapon=weapon, rings=(rings[1],)),
                    Fighter(weapon=weapon, rings=rings),
                    Fighter(weapon=weapon, armor=armor),
                    Fighter(weapon=weapon, armor=armor, rings=(rings[0],)),
                    Fighter(weapon=weapon, armor=armor, rings=(rings[1],)),
                    Fighter(weapon=weapon, armor=armor, rings=rings),
                ]
                for player in player_options:
                    boss = parse_boss(input)
                    winner = fight(player, boss)
                    if winner == "Boss" and player.build_cost > max_cost:
                        max_cost = player.build_cost
    print(f"Part 2 answer: {max_cost}")
    return max_cost


if __name__ == "__main__":
    input = get_data(day=21, year=2015)
    part1(input)
    part2(input)
