import random
import pandas as pd

class MDP:
    # MTD中等价异构体个数
    N = 10
    node_num = 0
    # 状态集合
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
    aggregate_utility = 0.0
    # Q值列表
    q_table = []
    # 最大修复主机数
    recover_max_num = 3

    debug = 0

    def __init__(self, bag):
        # TODO 根据配置读取行为以及各行为收益值
        self.bag = bag
        self.node_num = bag.node_num
        # print("Step 1 初始化状态集合")
        self.states_set = range(0, pow(2, self.node_num))
        # print(self.states_set)
        # print("Step 2 生成‘状态-行动’转移概率矩阵")
        self.generat_state_action_trans_prob_dict()
        # for i in range(len(self.actions_set)):
        #     print(self.actions_set[i])
        #     print(self.states_actions_trans_prob[i])

    def generat_state_action_trans_prob_dict(self):
        """根据贝叶斯攻击图中的一步转移概率，生成状态-动作转移概率"""
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
        # print('--------------------------------------------')

        str_current_state_bin = bin(current_state).split('b')[1].zfill(self.node_num)
        str_next_state_bin = bin(next_state).split('b')[1].zfill(self.node_num)
        # print(str_current_state_bin)
        # print(str_next_state_bin)
        # 节点0是攻击者的出发点
        current_state_1_list = [0]
        for i in range(1, self.node_num + 1):
            each_current_state = str_current_state_bin[self.node_num - i]
            if each_current_state == '1':
                current_state_1_list.append(i)
        for i in range(1, self.node_num + 1):
            # print('i=',i)
            each_current_state = str_current_state_bin[self.node_num - i]
            each_next_state = str_next_state_bin[self.node_num - i]
            # print(each_current_state,' ==  ',each_next_state)
            if each_current_state == '0' and each_next_state == '0':
                pro *= self.cal_failed_prob(current_state_1_list, i, action)
            elif each_current_state == '0' and each_next_state == '1':
                pro *= self.cal_access_prob(current_state_1_list, i) * self.actions_success_prob[action]
            elif each_current_state == '1' and each_next_state == '0':
                pro *= 1 - self.actions_success_prob[action]
            elif each_current_state == '1' and each_next_state == '1':
                pro *= self.actions_success_prob[action]
            else:
                pro *= 0
        # print('Pro = ',pro)
        return pro

    def cal_failed_prob(self, state_set, state, action):
        """
        根据从已占有节点集合计算到达目标节点失败的概率
        :param state_set:
        :param state:
        :return:
        """
        pro = 1
        for i in state_set:
            pro *= (1 - self.bag.trans_prob[i][state] * self.actions_success_prob[action])
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
        # print(state_set,'->',state)
        for i in state_set:
            # print("%s->%s=%f"%(i, state, self.bag.trans_prob[i][state]))
            if self.bag.trans_prob[i][state] > pro:
                pro = self.bag.trans_prob[i][state]
        # print("<-----最大概率是%f---------->"%(pro))
        # print(pro)
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

    def train(self):
        self.q_table = pd.DataFrame(data=[[0 for _ in self.actions_set] for _ in self.states_set],
                               index=self.states_set, columns=self.actions_set)
        for i in range(self.exp_time):
            self.qlearning(i)

    def qlearning(self, iter_num):
        # 随机选择起始状态，不可能以终止状态开始
        init_index = random.randint(0, len(self.states_set) - 2)
        current_state = self.states_set[init_index]
        total_step = 0
        # 每一轮采样的记录
        states_list = []
        actions_list = []
        rewards_list = []
        states_list.append(current_state)
        while self.states_set[len(self.states_set) - 1] != current_state and total_step < self.max_step:
            # 根据epsilon-greedy选择a
            current_action = self.epsilon_greedy(current_state)
            # 获取回报r和下一个状态s1
            next_state, utility = self.simulation(current_state, current_action)
            next_state_q_values = self.q_table.ix[next_state, self.get_valid_actions_list(next_state)]
            # 更新Q值函数
            self.q_table.ix[current_state, current_action] += self.alpha * (
                    utility + self.gamma * next_state_q_values.max() - self.q_table.ix[current_state, current_action])
            current_state = next_state
            total_step += 1
            states_list.append(current_state)
            actions_list.append(current_action)
            rewards_list.append(utility)
        # print("Episode ", iter_num)
        # print('state list', states_list)
        # print('action list', actions_list)
        # print('reward list', rewards_list)
        # print(self.q_table)
        return 0

    def epsilon_greedy(self, current_state):
        """epsilon贪婪策略:选取Action"""
        # 先找到最大动作
        action_max = self.q_table.ix[current_state].idxmax()
        # 概率选择部分
        pro = dict()
        valid_actions = self.get_valid_actions_list(current_state)
        for a in valid_actions:
            pro[a] = self.epsilon / len(valid_actions)
            if a == action_max:
                pro[a] += 1 - self.epsilon
        ## 根据概率分布选择动作
        r = random.uniform(0, 1)
        s = 0.0
        for a in valid_actions:
            s += pro[a]
            if s >= r:
                return a
        return a

    def simulation(self, state, action):
        """与模拟环境交互"""
        next_state = self.trans(state, action, 0)
        r = self.reward(state, action, next_state)
        return next_state, r

    def trans(self, current_state, current_action, flag):
        trans_table = self.states_actions_trans_prob[current_action][current_state]
        max_p = 0.0
        # 重新归一化
        for i in range(len(trans_table)):
            if flag == 1:
                # 增加随机扰动
                dv = random.uniform(0, 0.01)
                trans_table[i] += dv
            max_p += trans_table[i]
        r = random.uniform(0.0, max_p)
        s = 0.0
        for p in trans_table:
            s += p
            if s >= r:
                return trans_table.index(p)
        return len(trans_table) - 1

    def reward(self, current_state, action, next_state):
        """utility function"""
        r = self.TA(current_state) - self.TA(next_state) - self.eta * self.cost(current_state, action)
        return r

    def TA(self, state):
        threat = 0
        str_current_state_bin = bin(state).split('b')[1].zfill(self.node_num)
        for i in range(1, self.node_num + 1):
            each_current_state = str_current_state_bin[self.node_num - i]
            if each_current_state == '1':
                threat += self.bag.loss_value[i]
        return threat

    def cost(self, current_state, action):
        recover_num = 0
        str_current_state_bin = bin(current_state).split('b')[1].zfill(self.node_num)
        for i in range(1, self.node_num + 1):
            each_current_state = str_current_state_bin[self.node_num - i]
            if each_current_state == '1':
                recover_num += 1
        if action == 0:
            return 0
        elif action == 1:
            return 0.05 * recover_num
        elif action == 2:
            return 0.12 * recover_num
        elif action == 3:
            return 0.1 * recover_num
        elif action == 4:
            return 0.2 * recover_num
        elif action == 5:
            return 0.1 * (self.N + 2 * recover_num)
        else:
            return 0

    def make_decision(self, state):
        """返回指定状态下最大Q值动作"""
        return self.actions_set.index((self.q_table.ix[state].idxmax()))

    def environment(self, state, action):
        """真实环境模拟"""
        next_state = self.trans(state, action, 1)
        r = self.reward(state, action, next_state)
        return next_state, r

    def update_info(self, current_state, next_state, reward):
        """根据实际状态转移更新环境，并记录累积收益"""
        self.aggregate_utility *= self.gamma
        self.aggregate_utility += reward
        ap = self.get_attack_path(current_state, next_state)
        self.bag.update_trans_prob(ap)
        self.generat_state_action_trans_prob_dict()

    def get_attack_path(self, last_state, current_state):
        at_list = []
        str_last_state_bin = bin(last_state).split('b')[1].zfill(self.node_num)
        str_current_state_bin = bin(current_state).split('b')[1].zfill(self.node_num)
        for i in range(1, self.node_num + 1):
            each_last_state = str_last_state_bin[self.node_num - i]
            each_current_state = str_current_state_bin[self.node_num - i]
            if each_last_state == '0' and each_current_state == '1':
                at_list.append(i)
        return at_list