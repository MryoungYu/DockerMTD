from SDG.SDG import *
from SDG.Node import *
sdg = SDG()
sdg.generateSDGByDockerfile('dockerfile/tomcat_ubuntu')
print(sdg)
node1 = Node('1','2','3','4','5')
node2 = Node('1','2','3','4','5')
if node1 == node2:
    print('YES')
else:
    print('No')