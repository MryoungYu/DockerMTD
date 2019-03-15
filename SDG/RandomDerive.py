import SDG
import random

class RandomDerive:
    sdgs = []
    group_list = []
    root_list = []
    group_item_set = {}

    def __init__(self, sdgs):
        self.sdgs = sdgs
        for sdg in sdgs:
            group_list = sdg.group_list
            for group in  group_list:
                if group not in self.group_list:
                    self.group_list.append(group)
                    self.group_item_set[group] = []
                node_list_by_group = sdg.get_node_by_group(group)
            self.root_list += sdg.get_node_by_type('Sys')
        self.group_list = set(self.group_list)
        self.root_list = set(self.root_list)

    def exec(self):
        r = random.randint()
        # 从根节点中随机选取一个作为新的根节点
        new_root_node  = self.root_list[r]