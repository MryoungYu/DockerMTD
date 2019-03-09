import sys
import random

states = [0,1,2,3,4,5,6,7]
actions = ['n', 'e', 's', 'w']

N = 10

alpha = 1
gamma = 0.8
epsilon = 0.7
eta = 0.8

exp_time = 13
max_step = 100

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

def qlearning(iter, alpha, epsilon):
    """
    Qlearning 策略改善
    探索策略：epsilon贪婪策略
    值函数更新策略：贪婪策略
    """
    # 初始化Q值函数
    qfunc = dict()
    for s in states:
        for a in actions:
            key = "%d_%s"%(s, a)
            qfunc[key] = 0.0
    # 终止状态标识
    t = False
    # 策略迭代轮次
    count = 0
    # 选择起始s
    r = random.randint(0, len(states)-1)
    s = states[r]
    # 根据epsilon-greedy选择a
    a = epsilon_greedy(qfunc, s, epsilon)
    while False == t and count < 100:
        key = "%d_%s"%(s,a)
        # 获取回报r和下一个状态s1
        t,s1,r = simulation(s,a)
        print("State:", count, "=", s)
        print("Action ", count, "=", a)
        print("Reward ", count, "=", r)
        rewards.append(r)
        key1 = ""
        qmax = -1.0
        # 为s1选择q值最大的行动a1
        for a1 in actions:
            if qmax < qfunc["%d_%s"%(s1, a1)]:
                qmax = qfunc["%d_%s"%(s1, a1)]
                key1 = "%d_%s"%(s1, a1)
        # 更新Q值函数
        qfunc[key] = qfunc[key] + alpha * (r + gamma * qfunc[key1] - qfunc[key])
        s = s1
        a = epsilon_greedy(qfunc, s1, epsilon)
        count += 1
    return qfunc


def epsilon_greedy(qfunc, state, epsilon):
    """epsilon贪婪策略"""
    # 先找到最大动作
    amax = 0
    key = "%d_%s"%(state, actions[0])
    qmax = qfunc[key]
    for i in range(len(actions)):   # 扫描动作空间得到最大动作值函数
        key = "%d_%s"%(state, actions[i])
        q = qfunc[key]
        if qmax < q:
            qmax = q
            amax = i
    # 概率部分
    pro = [0.0 for i in range(len(actions))]
    pro[amax] += 1 - epsilon
    for i in range(len(actions)):
        pro[i] += epsilon / len(actions)
    ## 根据概率分布选择动作
    r = random.random()
    s = 0.0
    for i in range(len(actions)):
        s += pro[i]
        if s >= r:
            return actions[i]
    return actions[len(actions) - 1]

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
    s1 = trans(s, a)
    r = reward(s, a, s1, 0.8)

    t = False
    if s1 == 1:
        t = True
    return t, s1, r

def reward(s, a, s1, eta):
    r = threat(s1) - threat(s) - k*cost(a)
    return r

def threat(s):
    return 0

def cost(a):
    return 1

def trans(s, a):
    return s % len(states) + 1

if __name__=="__main__":
    print("main")
    qlearning(0.5, 0.5)
