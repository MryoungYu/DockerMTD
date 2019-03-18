from SDG.SDG import SDG
from SDG.RandomDerive import RandomDerive

# 根据DockerFile生成SDG
print("Generating System Dependence Graphs")
sdg1 = SDG()
sdg1.generateSDGByDockerfile('dockerfile/apache_mysql_centos6.3')
sdg1.draw_graph()
print("SDG1 DONE")

sdg2 = SDG()
sdg2.generateSDGByDockerfile('dockerfile/apache_mysql_ubuntu')
sdg2.draw_graph()
print("SDG2 DONE")

# 组成SDG列表，执行随机派生算法
sdg_list = [sdg1, sdg2]

rd = RandomDerive(sdg_list)
new_sgdg_list = rd.exec(1)
new_sdg_list = []
for i in range(len(new_sgdg_list)):
    print('RD new SDG '+ str(i))
    sgdg = new_sgdg_list[i]
    sdg = SDG()
    sdg.generate_by_SGDG(sgdg)
    sdg.SDG_name = 'RD-'+ str(i)
    print(sdg)
    sdg.draw_graph()
    new_sdg_list.append(sdg)
for new_sdg in new_sdg_list:
    new_sdg.generate_dockerfile()
