# 测试增量修复IR机制

from SDG.SDG import *
from SDG.Node import *
from SDG.IncrementalRecover import *
import time

sdg = SDG()
sdg.generateSDGByDockerfile('dockerfile/test_for_cost_20')
print(sdg)
recover_condition = sdg.node_set['node2']
recover_node = Node('Add Patch', 'CVE', 'Conf', recover_condition.node_group, ['ADD recover.sh', 'CMD[recover.sh]'])
IR = IncrementalRecover(sdg, recover_condition, recover_node)
start_time = time.time()
print(IR.exec())
end_time = time.time()
print("IR Cost = " + str(end_time - start_time))
IR.sdg.SDG_name += '_recovered'
start_time = time.time()
IR.sdg.generate_dockerfile()
end_time = time.time()
print("Generate Dockerfile Cost = " + str(end_time - start_time))