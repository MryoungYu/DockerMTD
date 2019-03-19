from SDG.SDG import SDG
from SDG.RandomDerive import RandomDerive
import time

# 根据DockerFile生成SDG
print("Generating System Dependence Graphs")
base = "dockerfile/RD-"
sdg_list = []
for i in range(1, 11):
    sdg = SDG()
    filepath = base + str(i)
    sdg.generateSDGByDockerfile(filepath)
    sdg_list.append(sdg)
print("SDG List Load Complete")
rd = RandomDerive(sdg_list)
start_time = time.time()
new_sgdg_list, r_list, r_num = rd.exec(50)
end_time = time.time()
print("repeat num = " + str(r_num))
print(r_list)
print("RD Cost : " + str(end_time - start_time))
# for i in range(len(new_sgdg_list)):
#     print('RD new SDG '+ str(i))
#     sgdg = new_sgdg_list[i]
#     sdg = SDG()
#     sdg.generate_by_SGDG(sgdg)
#     sdg.SDG_name = 'RD-'+ str(i)
#     print(sdg)
