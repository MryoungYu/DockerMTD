from SDG.SDG import *
sdg = SDG()
sdg.generateSDGByDockerfile('dockerfile/tomcat')
print(sdg)