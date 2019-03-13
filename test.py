from BAG.BAG import *
from MDP.MDP import *
import time

bag = BAG()
mdp = MDP(bag)
state = 0
count = 0
reward_list = []
while state != pow(2, mdp.node_num) - 1 or count <= 100:
    print("Round ",count)
    print("Traning...")
    time_start = time.time()
    mdp.train()
    time_end = time.time()
    print("Trainging Over : ",time_end - time_start)
    action = mdp.make_decision(state)
    print("Make Decision: state = ", state, "action = ", mdp.actions_set[action])
    next_state, reward = mdp.environment(state, action)
    print("Interact with System: next state is %d, reward in this round is %f"%(next_state, reward))
    reward_list.append(reward)
    print("Updating Assessment System...")
    time_start = time.time()
    mdp.update_info(state, next_state, reward)
    time_end = time.time()
    print("Updating Done : ", time_end - time_start)
    print("Aggregate Utility is ", mdp.aggregate_utility)
    state = next_state
    count += 1
    print('--------------------------------------------------------------')

print("Reward List : ",reward_list)
