from SDG.SDG import *
from SDG.Node import *
sdg = SDG()
sdg.generateSDGByDockerfile('dockerfile/tomcat')
print(sdg)
node1 = Node('1','2','3','5')
node2 = Node('1','2','3','5')
if node1 == node2:
    print('YES')
else:
    print('No')