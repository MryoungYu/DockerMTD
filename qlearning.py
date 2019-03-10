import random
import pandas as pd

# 状态集合S
states = ['NORMAL', 'SINGLE_NONE', 'SINGLE_LOW', 'SINGE_HIGH', 'MULTI_NONE', 'MULTI_LOW', 'MULTI_HIGH']
# 行动集合A
actions = ['NONE', 'TRANS', 'RECOVER', 'RESET', 'RD', 'GA']
# 每个状态的可用行为At
valid_actions = {
    'NORMAL':['NONE', 'TRANS', 'GA'],
    'SINGLE_NONE':['NONE', 'TRANS', 'RESET', 'RD', 'GA'],
    'SINGLE_LOW':['NONE', 'TRANS', 'RECOVER', 'RESET', 'RD', 'GA'],
    'SINGE_HIGH':['NONE', 'TRANS', 'RECOVER', 'RESET', 'RD', 'GA'],
    'MULTI_NONE':['NONE', 'TRANS', 'RESET', 'RD', 'GA'],
    'MULTI_LOW':['NONE', 'TRANS', 'RECOVER', 'RESET', 'RD', 'GA'],
    'MULTI_HIGH':['NONE', 'TRANS', 'RECOVER', 'RESET', 'RD', 'GA'],
}
# 每个状态对应的威胁值T(S)
threat_table = {
    'NORMAL':0,
    'SINGLE_NONE': 0.1,
    'SINGLE_LOW' : 0.2,
    'SINGE_HIGH' : 0.3,
    'MULTI_NONE' : 0.2,
    'MULTI_LOW' : 0.5,
    'MULTI_HIGH' : 0.8,
}
# 每个行为的运行成本C(A)
cost_table = {
    'SINGLE_NONE+NONE'   :[0.5, 0.3, 0.1, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+TRANS'  :[0.6, 0.3, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+RESET'  :[0.7, 0.2, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+RD'     :[0.7, 0.2, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+GA'     :[0.7, 0.2, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+NONE'    :[0.1, 0.3, 0.3, 0.2, 0.1, 0.0, 0.0],
    'SINGLE_LOW+TRANS'   :[0.3, 0.5, 0.2, 0.0 , 0.0, 0.0, 0.0],
    'SINGLE_LOW+RECOVER' :[0.6, 0.2, 0.1, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+RESET'    :[0.5, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+RD'        :[0.5, 0.3, 0.1, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+GA'        :[0.5, 0.4, 0.1, 0.0, 0.0, 0.0, 0.0],
    'SINGE_HIGH+NONE'      :[0.0, 0.1, 0.1, 0.6, 0.0, 0.1, 0.1],
    'SINGE_HIGH+TRANS'     :[0.3, 0.3, 0.2, 0.1, 0.1, 0.0, 0.0],
    'SINGE_HIGH+RECOVER'   :[0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0],
    'SINGE_HIGH+RESET'     :[0.3, 0.1, 0.2, 0.2, 0.1, 0.1, 0.0],
    'SINGE_HIGH+RD'         :[0.5, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0],
    'SINGE_HIGH+GA'         :[0.6, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0],
    'MULTI_NONE+NONE'       :[0.5, 0.1, 0.0, 0.0, 0.3, 0.1, 0.0],
    'MULTI_NONE+TRANS'      :[0.6, 0.1, 0.0, 0.0, 0.3, 0.0, 0.0],
    'MULTI_NONE+RESET'      :[0.7, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0],
    'MULTI_NONE+RD'         :[0.7, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0],
    'MULTI_NONE+GA'         :[0.7, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0],
    'MULTI_LOW+NONE'        :[0.1, 0.1, 0.0, 0.0, 0.3, 0.3, 0.2],
    'MULTI_LOW+TRANS'       :[0.3, 0.0, 0.0, 0.0 , 0.5, 0.2, 0.0],
    'MULTI_LOW+RECOVER'     :[0.6, 0.1, 0.0, 0.0, 0.2, 0.1, 0.0],
    'MULTI_LOW+RESET'       :[0.5, 0.1, 0.0, 0.0, 0.2, 0.2, 0.0],
    'MULTI_LOW+RD'          :[0.5, 0.1, 0.0, 0.0, 0.3, 0.1, 0.0],
    'MULTI_LOW+GA'          :[0.5, 0.0, 0.0, 0.0, 0.4, 0.1, 0.0],
    'MULTI_HIGH+NONE'      :[0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 0.6],
    'MULTI_HIGH+TRANS'     :[0.3, 0.0, 0.0, 0.0, 0.1, 0.4, 0.2],
    'MULTI_HIGH+RECOVER'   :[0.4, 0.0, 0.0, 0.0, 0.3, 0.2, 0.1],
    'MULTI_HIGH+RESET'     :[0.3, 0.0, 0.0, 0.0, 0.2, 0.3, 0.2],
    'MULTI_HIGH+RD'         :[0.5, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0],
    'MULTI_HIGH+GA'         :[0.6, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0],
}
# 状态-行动转移概率矩阵
trans_matrix = {
    'SINGLE_NONE+NONE'   :[0.5, 0.3, 0.1, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+TRANS'  :[0.6, 0.3, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+RESET'  :[0.7, 0.2, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+RD'     :[0.7, 0.2, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_NONE+GA'     :[0.7, 0.2, 0.0, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+NONE'    :[0.1, 0.3, 0.3, 0.2, 0.1, 0.0, 0.0],
    'SINGLE_LOW+TRANS'   :[0.3, 0.5, 0.2, 0.0 , 0.0, 0.0, 0.0],
    'SINGLE_LOW+RECOVER' :[0.6, 0.2, 0.1, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+RESET'    :[0.5, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+RD'        :[0.5, 0.3, 0.1, 0.0, 0.1, 0.0, 0.0],
    'SINGLE_LOW+GA'        :[0.5, 0.4, 0.1, 0.0, 0.0, 0.0, 0.0],
    'SINGE_HIGH+NONE'      :[0.0, 0.1, 0.1, 0.6, 0.0, 0.1, 0.1],
    'SINGE_HIGH+TRANS'     :[0.3, 0.3, 0.2, 0.1, 0.1, 0.0, 0.0],
    'SINGE_HIGH+RECOVER'   :[0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0],
    'SINGE_HIGH+RESET'     :[0.3, 0.1, 0.2, 0.2, 0.1, 0.1, 0.0],
    'SINGE_HIGH+RD'         :[0.5, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0],
    'SINGE_HIGH+GA'         :[0.6, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0],
    'MULTI_NONE+NONE'       :[0.5, 0.1, 0.0, 0.0, 0.3, 0.1, 0.0],
    'MULTI_NONE+TRANS'      :[0.6, 0.1, 0.0, 0.0, 0.3, 0.0, 0.0],
    'MULTI_NONE+RESET'      :[0.7, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0],
    'MULTI_NONE+RD'         :[0.7, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0],
    'MULTI_NONE+GA'         :[0.7, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0],
    'MULTI_LOW+NONE'        :[0.1, 0.1, 0.0, 0.0, 0.3, 0.3, 0.2],
    'MULTI_LOW+TRANS'       :[0.3, 0.0, 0.0, 0.0 , 0.5, 0.2, 0.0],
    'MULTI_LOW+RECOVER'     :[0.6, 0.1, 0.0, 0.0, 0.2, 0.1, 0.0],
    'MULTI_LOW+RESET'       :[0.5, 0.1, 0.0, 0.0, 0.2, 0.2, 0.0],
    'MULTI_LOW+RD'          :[0.5, 0.1, 0.0, 0.0, 0.3, 0.1, 0.0],
    'MULTI_LOW+GA'          :[0.5, 0.0, 0.0, 0.0, 0.4, 0.1, 0.0],
    'MULTI_HIGH+NONE'      :[0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 0.6],
    'MULTI_HIGH+TRANS'     :[0.3, 0.0, 0.0, 0.0, 0.1, 0.4, 0.2],
    'MULTI_HIGH+RECOVER'   :[0.4, 0.0, 0.0, 0.0, 0.3, 0.2, 0.1],
    'MULTI_HIGH+RESET'     :[0.3, 0.0, 0.0, 0.0, 0.2, 0.3, 0.2],
    'MULTI_HIGH+RD'         :[0.5, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0],
    'MULTI_HIGH+GA'         :[0.6, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0],
}
# 初始化Q值表
q_table = pd.DataFrame(data=[[0 for _ in actions] for _ in states],
                       index=states, columns=actions)
# 等价异构体个数，环境参数
N = 10
# 承受系数，环境参数
eta = 0.8
# 学习率
alpha = 1
# 折扣因子
gamma = 0.8
# 贪婪度
epsilon = 0.7
# 采样数
exp_time = 13
# 最大步长
max_step = 100
# 累积收益
aggregate_utility = 0.8

# def td(alpha, gamma, state_sample, action_sample, reward_sample):
#     """时间差分方法评估"""
#     vfunc = dict()
#     for s in states:
#         vfunc[s] = random.random()
#     for iter1 in range(len(state_sample)):
#         for step in range(len(state_sample[iter1])):
#             s = state_sample[iter1][step]
#             r = reward_sample[iter1][step]
#             if len(state_sample[iter1]) - 1 > step:
#                 s1 = state_sample[iter1][step + 1]
#                 next_v = vfunc[s1]
#             else:
#                 next_v = 0.0
#             vfunc[s] = vfunc[s] + alpha * (r + gamma * next_v - vfunc[s])

def qlearning(iter):
    """
    Qlearning 策略改善
    探索策略：epsilon贪婪策略
    值函数更新策略：贪婪策略
    """
    # 序列
    states_list = []
    actions_list = []
    rewards_list = []
    # 终止状态标识
    flag = False
    # 选择起始s
    init_index = random.randint(0, len(states)-1)
    current_state = states[init_index]
    total_step = 0
    states_list.append(current_state)
    while 'NORMAL' != current_state and total_step < max_step:
        # 根据epsilon-greedy选择a
        current_action = epsilon_greedy(current_state)
        # 获取回报r和下一个状态s1
        next_state,utility = simulation(current_state, current_action)
        next_state_q_values = q_table.ix[next_state, valid_actions[next_state]]
        # 更新Q值函数
        q_table.ix[current_state, current_action] += alpha * (
                utility + gamma * next_state_q_values.max() - q_table.ix[current_state, current_action])
        current_state = next_state
        total_step += 1
        states_list.append(current_state)
        actions_list.append(current_action)
        rewards_list.append(utility)
    print("Stats:", states_list)
    print("Actions:", actions_list)
    print("Rewards:", rewards_list)
    print("Q-TABLE:", q_table)
    return 0


def epsilon_greedy(current_state):
    """epsilon贪婪策略:选取Action"""
    # 先找到最大动作
    action_max = q_table.ix[current_state].idxmax()
    # 概率部分
    pro = dict()
    for a in valid_actions[current_state]:
        pro[a] = epsilon / len(valid_actions[current_state])
        if a == action_max:
            pro[a] += 1 - epsilon

    ## 根据概率分布选择动作
    r = random.uniform(0, 1)
    s = 0.0
    for a in valid_actions[current_state]:
        s += pro[a]
        if s >= r:
            return a
    return a

def greedy(qfunc, state):
    """贪婪策略"""
    amax = 0
    key = "%d_%s"%(state, actions[0])
    qmax = qfunc[key]
    for i in range(len(actions)):
        key = "%d_%s"%(state, actions[i])
        q = qfunc[key]
        if qmax < q:
            qmax = q
            amax = i
    return actions[amax]

def simulation(s, a):
    """模拟与环境交互"""
    next_state = trans(s, a)
    r = reward(s, a, next_state)
    return next_state, r

def reward(current_state, action, next_state):
    """utility function"""
    r = TA(current_state) - TA(next_state) - eta*cost(current_state, action)
    return r

def TA(s):
    """Threat Assessment Function"""
    return threat_table[s]

def cost(s, a):
    if 'NONE' == a:
        return 0
    if 'TRANS' == a:
        return 0.05
    if 'RECOVER' == a:
        if s.startswith('MULTI'):
            return 0.3
        else:
            return 0.1
    if 'RESET' == a:
        if s.startswith('MULTI'):
            return 0.5
        else:
            return 0.2
    if 'RD' == a:
        return 0.4
    if 'GA' == a:
        return 0.6
    return 0

def trans(current_state, current_action):
    key = "%s+%s"%(current_state, current_action)
    trans_table = trans_matrix[key]
    # 增加随机概率扰动
    max_p = 1.0
    for i in range(0, len(trans_table)):
        dv = random.uniform(0, 0.1)
        trans_table[i] += dv
        max_p += dv
    r = random.uniform(0, max_p)
    s = 0.0
    for p in trans_table:
        s += p
        if s >= r:
            return states[trans_table.index(p)]
    return states[len(states) - 1]

if __name__=="__main__":
    print("Q Learning Function")
    for i in range(exp_time):
        print("Episode %d:" % (i))
        qlearning(i)
    print("Q-Table:", q_table)
