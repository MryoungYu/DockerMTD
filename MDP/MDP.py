class MDP:
    # MTD中等价异构体个数
    N = 3
    states_set = []
    # 行动集合
    actions_set = ['NONE', 'TRANS', 'RECOVER', 'RESET', 'RD', 'GA']
    # 贝叶斯攻击图
    bag = False
    # 防守行为可以降低攻击者的成功概率，即P(S'|s, a) = P(s'|s)*P(a)
    actions_success_prob = [1.0, 0.9, 0.7, 0.6, 0.5, 0.3]
    states_actions_trans_prob = []
    # 折扣因子
    gamma = 0.8
    # 承受系数，环境参数
    eta = 0.8
    # 学习率
    alpha = 0.8
    # 贪婪度
    epsilon = 0.7
    # 采样数
    exp_time = 1000
    # 最大步长
    max_step = 100
    # 累积收益
    aggregate_utility = 0.8


    def __init__(self, bag):
        # TODO 根据配置读取行为以及各行为收益值
        self.bag = bag
        self.node_num = bag.node_num
        print("Step 1 初始化状态集合")
        self.states_set = range(0, pow(2, self.node_num)-1)
        print(self.states_set)
        print("Step 2 生成‘状态-行动’转移概率矩阵")
        for a in range(len(self.actions_set)):
            each_action_state_prob = []
            for i in self.states_set:
                each_action_each_state_prob = []
                for j in self.states_set:
                    each_action_each_state_prob.append(self.cal_state_action_prob(i, j, a))
                each_action_state_prob.append(each_action_each_state_prob)
            self.states_actions_trans_prob.append(each_action_state_prob)


    def cal_state_action_prob(self, current_state, next_state, action):
        pro = 1
        better_set = []
        worse_set = []
        str_current_state_bin = bin(current_state).split('b')[1].zfill(self.node_num)
        str_next_state_bin = bin(next_state).split('b')[1].zfill(self.node_num)
        # print('current_state_str=',str_current_state_bin)
        # print('next_state_str=',str_next_state_bin)
        # 节点0是攻击者的出发点
        current_state_1_list = [0]
        for i in range(1, self.node_num):
            each_current_state = str_current_state_bin[self.node_num - i]
            each_next_state = str_next_state_bin[self.node_num - i]
            if each_current_state == '1':
                current_state_1_list.append(i)
                if each_next_state == '0':
                    better_set.append(i)
            if each_current_state == '0' and each_next_state == '1':
                worse_set.append(i)
        # print('worse_set=',worse_set)
        # print('better_set',better_set)
        # print('bad_set=',current_state_1_list)
        for i in worse_set:
            pro *= self.cal_access_prob(current_state_1_list, i) * self.actions_success_prob[action]
        pro *= pow((1 - self.actions_success_prob[action]), len(better_set))
        return pro

    def cal_access_prob(self, state_set, state):
        """
        根据已占有节点集合计算目标节点的一步可达概率
        :param state_set:已有节点集合
        :param state:目标节点
        :return:最大概率
        """
        # print(">-----计算最大可达概率-------<")
        # print("起点集合",state_set)
        # print("终点",state)
        pro = 0
        for i in state_set:
            # print("%s->%s=%f"%(i, state, self.bag.trans_prob[i][state]))
            if self.bag.trans_prob[i][state] > pro:
                pro = self.bag.trans_prob[i][state]
        # print("<-----最大概率是%f---------->"%(pro))
        return pro

    def cal_action_cost(self, action, n):
        """
        行动开销计算
        :param action:行动编号
        :param n:影响主机个数
        :return:成本值
        """
        if action == 0:
            return 0
        elif action == 1:
            return 0.5 * n
        elif action == 2:
            return 1.2 * n
        elif action == 3:
            return n
        elif action == 4:
            return 2 * n
        elif action == 5:
            return (self.node_num - n) + (2 * n + n)

    # def cal_reward(self, current_state, next_state, action):

    def get_valid_actions_list(self, state):
        """获取每个状态可用的行动集合"""
        if state == 0:
            return [0]
        else:
            return range(len(self.actions_set))

    def qlearning(self):