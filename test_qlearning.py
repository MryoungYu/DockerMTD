state_list = [0, 1, 2, 3]
action_list = [0, 1]

def get_prob(state, action):
    if action == 0:
        if state == 0:
            return {
                0 : 0.04,
                1 : 0.8,
                2 : 0.8,
                3 : 0.64,
            }
        if state == 1:
            return {
                0 : 0,
                1 : 0.2,
                2 : 0,
                3 : 0.8,
            }
        if state == 2:
            return {
                0 : 0,
                1 : 0,
                2 : 0.2,
                3 : 0.8,
            }
        if state == 3:
            return {
                0 : 0,
                1 : 0,
                2 : 0,
                3 : 1,
            }
    if action == 1:
        if state == 0:
            return {
                0 : 0.64,
                1 : 0.2,
                2 : 0.2,
                3 : 0.04,
            }
        if state == 1:
            return {
                0 : 0.8,
            }