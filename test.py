from BAG.BAG import *
from MDP.MDP import *
import time

bag = BAG()
mdp = MDP(bag)
state = 0
count = 0
reward_list = []
f = open('result.txt', 'a')
while state != pow(2, mdp.node_num) - 1 or count <= 100:
    print(count)
    f.write("Round %d\r\n"%(count))
    f.write("Traning...\r\n")
    time_start = time.time()
    mdp.train()
    time_end = time.time()
    f.write("Trainging Over : %s\r\n"%(time_end - time_start))
    action = mdp.make_decision(state)
    f.write("Make Decision: state = "+ str(state)+ "action = "+ mdp.actions_set[action] + "\r\n")
    next_state, reward = mdp.environment(state, action)
    f.write("Interact with System: next state is %d, reward in this round is %f\r\n"%(next_state, reward))
    reward_list.append(reward)
    f.write("Updating Assessment System...\r\n")
    time_start = time.time()
    mdp.update_info(state, next_state, reward)
    time_end = time.time()
    f.write("Updating Done : "+str(time_end - time_start) + "\r\n")
    f.write("Aggregate Utility is "+ str(mdp.aggregate_utility) + "\r\n")
    state = next_state
    count += 1
    f.write("--------------------------------------------------------------\r\n")

print(reward_list)
f.close()
