import SGDG
import random

class RandomDerive:
    gdg_num = 0
    group_list = []
    root_list = []
    gdg_dict = {}

    def __init__(self, sdgs):
        self.gdg_num = len(sdgs)
        for sdg in sdgs:
            sgdg = sdg.change_to_sgdg()
            group_list = sgdg.group_list
            for group in  group_list:
                if group not in self.group_list:
                    self.group_list.append(group)
                    self.gdg_list[group] = []
                self.gdg_dict[group].append(sgdg.gdg_dict[group])
            self.root_list += sgdg.root_node

    def exec(self, n):
        """
        随机派生执行入口
        :param n: 执行轮次
        :return:派生的SDG数组，以SGDG形式返回
        """
        sgdg_list = []
        for i in range(n):
            r = random.randint(self.gdg_num)
            # 从根节点中随机选取一个作为新的根节点
            new_root_node  = self.root_list[r]
            new_gdg_dict = {}
            for group in self.group_list:
                # 为每个分组随机选取
                r = random.randint(self.gdg_num)
                new_gdg_dict[group] = self.gdg_dict[group][r]
            sgdg = SGDG(new_root_node, new_gdg_dict)
            sgdg_list.append(sgdg)
        return sgdg_list
