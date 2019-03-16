from SDG.SDG import *
from SDG.RandomDerive import *

# 根据DockerFile生成SDG
sdg1 = SDG()
sdg1.generateSDGByDockerfile('dockerfile/tomcat_ubuntu')
print(sdg1)

sdg2 = SDG()
print(sdg2)
sdg2.generateSDGByDockerfile('dockerfile/tomcat_centos')
print(sdg2)

sdg_list = [sdg1, sdg2]

rd = RandomDerive(sdg_list)
new_sgdg_list = rd.exec(1)
new_sdg_list = []
for sgdg in new_sgdg_list:
    sdg = sgdg.change_to_sdg()
    new_sgdg_list.append(sdg)
for sdg in sdg_list: