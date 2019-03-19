from SDG.SGDG import SGDG
import random

class RandomDerive:
    gdg_num = 0
    group_list = []
    root_list = []
    gdg_dict = {}

    def __init__(self, sdgs):
        self.gdg_num = len(sdgs)
        self.group_list = list()
        self.root_list = list()
        self.gdg_dict = dict()
        for sdg in sdgs:
            sgdg = sdg.change_to_sgdg()
            group_list = sgdg.group_list
            for group in  group_list:
                if group not in self.group_list:
                    self.group_list.append(group)
                    self.gdg_dict[group] = []
                self.gdg_dict[group].append(sgdg.gdg_dict[group])
            self.root_list.append(sgdg.root_node)

    def exec(self, n):
        """
        随机派生执行入口
        :param n: 执行轮次
        :return:派生的SDG数组，以SGDG形式返回
        """
        sgdg_list = []
        r_list = list()
        r_num = 0
        # random.seed(111)
        # print(self.gdg_num)
        # print(self.group_list)
        # print(self.root_list)
        i = 0
        while (len(r_list) < n):
            # r = random.random()
            # r = int(r * 10)
            # r = random.randint(0, self.gdg_num-1)
            # print(r)
            # 从根节点中随机选取一个作为新的根节点
            new_root_node = random.choice(self.root_list)
            # new_root_node  = self.root_list[r]
            new_gdg_dict = {}
            r_str = ''
            for group in self.group_list:
                # 为每个分组随机选取
                # r = random.random()
                # r = int(r * 10)
                # r = random.randint(0, self.gdg_num-1)
                new_gdg_dict[group] = random.choice(self.gdg_dict[group])
                r_str += str(self.gdg_dict[group].index(new_gdg_dict[group]))
                # new_gdg_dict[group] = self.gdg_dict[group][r]
            if r_str in r_list:
                r_num += 1
                # print(r_str)
                if i > 0:
                    i = i - 1
            else:
                i = i + 1
                r_list.append(r_str)
                sgdg = SGDG(new_root_node, new_gdg_dict)
                sgdg_list.append(sgdg)
        return sgdg_list,r_list, r_num
