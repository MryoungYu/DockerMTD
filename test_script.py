from SDG.SDG import *
import time
from SDG.Node import *
sdg = SDG()
# start_time = datetime.datetime.now()
start_time = time.time()
sdg.generateSDGByDockerfile('dockerfile/test_for_cost_20')
# end_time = datetime.datetime.now()
end_time = time.time()
print("Generate SDG From Dockerfile:" + str((end_time - start_time)))
start_time = time.time()
# start_time = datetime.datetime.now()
sdg.draw_graph()
end_time = time.time()
# end_time = datetime.datetime.now()
print("Draw SDG Graph From SDG Data:" + str((end_time - start_time)))