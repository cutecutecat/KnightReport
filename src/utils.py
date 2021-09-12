import csv
from typing import Sequence, Dict, List


class Info:
    def __init__(self, uid: int, name: str, days: int):
        self.uid: int = uid
        self.name: str = name
        self.hits: int = 0
        self.kill: int = 0
        self.damage: int = 0
        self.not_killed_damage: int = 0
        self.boss_hits: Dict[str, int] = {}
        self.boss_damage: Dict[str, int] = {}
        # omit can be [-3, 0], -x equals omit x hit one day
        self.omission: List[int] = [0] * days

    @staticmethod
    def omit_mapping(x: int):
        if x == 0:
            return ""
        else:
            return str(x)

    def add_hit(self, boss_target: str, damage: int, killed: int):
        if killed == 0:
            self.not_killed_damage += damage
        elif killed == 1:
            self.kill += 1
        else:
            raise ValueError
        if not self.boss_hits.__contains__(boss_target):
            self.boss_hits[boss_target] = 1
            self.boss_damage[boss_target] = damage
        else:
            self.boss_hits[boss_target] += 1
            self.boss_damage[boss_target] += damage

    def to_list(self, boss_names: Sequence[str]):
        boss_status = []
        for name in boss_names:
            if self.boss_hits.__contains__(name):
                boss_status.extend([self.boss_hits[name], self.boss_damage[name]])
            else:
                boss_status.extend([0, 0])

        date_status = [self.omit_mapping(omit) for omit in self.omission]

        avg_damage = '{:d}'.format(
            self.not_killed_damage // (self.hits - self.kill)) if self.hits - self.kill > 0 else '-'
        status = [self.uid, self.name, self.hits, self.damage, self.kill, avg_damage]
        status.extend(boss_status)
        status.extend(date_status)
        return status

    def __repr__(self):
        return str(self.__dict__)

    def __lt__(self, other):
        if self.hits != other.hits:
            return self.hits > other.hits
        elif self.damage != other.damage:
            return self.damage > other.damage
        return 0


class Combat:
    def __init__(self, dates: Sequence[str]):
        self.dates = dates
        self.boss_name = list()
        self._boss_set = set()

    def has_boss(self, name: str):
        return self._boss_set.__contains__(name)

    def add_boss(self, name: str):
        if not self.has_boss(name):
            self.boss_name.append(name)
            self._boss_set.add(name)

    def marshal(self, person_list: Sequence[Info], filename: str):
        headers = ["uid", "玩家", "出刀", "伤害", "尾刀", "均伤(除尾刀)"]

        for boss in self.boss_name:
            headers.extend(["{:s}出刀".format(boss), "{:s}伤害".format(boss)])
        headers.extend("{:s}漏刀".format(date) for date in self.dates)

        person_list = sorted(person_list)
        rows = [person.to_list(self.boss_name) for person in person_list]
        with open(filename, 'w', encoding='utf_8_sig') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)
