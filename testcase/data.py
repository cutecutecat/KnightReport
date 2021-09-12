from random import randint
from typing import Dict


class TestData:
    user_id_range = [1000000000, 2000000000]
    provided_names = ['一方通行', '未元物质', '超电磁炮', '原子崩坏', '心理掌握',
                      '存在缺失', '倚云桑', 'ろい', '皓烁', '是你的嘉云呀',
                      '潍胤', '无影惜梦', '乌雅乐家', '日允', '骞暄',
                      '第七绮文', '乐羊楠楠', '彬彬', '阿伟', '杰哥',
                      '陈少龙', '东仙队长', '人类高质量男性', '你', 'FBI',
                      'na@na', '42', '田所浩二', '福瑞控', '蒙古上单']

    def __init__(self):
        # generate num user
        self.num = 30
        self.ids = set()
        self.names = set()
        while len(self.ids) < self.num:
            self.ids.add(randint(self.user_id_range[0], self.user_id_range[1]))
        while len(self.names) < self.num:
            if len(self.names) < len(self.provided_names):
                self.names.add(self.provided_names[len(self.names)])
            else:
                self.names.add(str(randint(10000, 99999)))

        self.ids = list(self.ids)
        self.names = list(self.names)

    @property
    def attack_data(self) -> Dict:
        from template import template_attack_data
        attack_data = template_attack_data
        for i in range(len(attack_data['data'])):
            attack_data['data'][i]['user_id'] = self.ids[i]
            attack_data['data'][i]['user_name'] = self.names[i]
        return attack_data

    @property
    def guild_data(self) -> Dict:
        from template import template_guild_data
        guild_data = template_guild_data
        for i in range(len(guild_data['data']['member'])):
            guild_data['data']['member'][i]['id'] = self.ids[i]
            guild_data['data']['member'][i]['name'] = self.names[i]
        return guild_data
