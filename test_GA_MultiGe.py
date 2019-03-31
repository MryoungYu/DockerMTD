from SDG.Chromosome import *
import random
import time

# print("生成安全事件队列")
# for i in range(10):
#     num = random.randint(1, 3)
#     threat = random.randint(1, 3)
#     print("时间周期"+str(i)+"："+str(num)+"个染色体有安全问题,"+"安全事件的威胁等级为"+str(threat))
#
#     for j in range(num):
#         r = random.randint(1, 10)
#         print(r)

"""
安全事件序列：
0' 威胁等级3，涉及染色体：2,4,9
1' 威胁等级3，涉及染色体：1,10
2' 威胁等级3：涉及染色体：5
3' 威胁等级3：涉及染色体：5
4' 威胁等级1，涉及染色体：6,7
5' 威胁等级2，涉及染色体：9
6' 威胁等级1，涉及染色体：4,8,10
7' 威胁等级3，涉及染色体：4
8' 威胁等级2，涉及染色体：7,8,10
9' 威胁等级1，涉及染色体：2
"""

# 1. 生成10组染色体的基因序列
# 2. 选择5个适应度最高的进入下一生代
# 3. 从10个染色体中概率选择两个
# 4. 从两个染色体中概率选择基因，组成新染色体
# 5. 变异
# 6. 检查染色体
# 7. 若合格染色体不足5个： GOTO 3
# 8. 若合格染色体满足5个：计算当前生代的基因个数，计算当前生代的平均威胁值(基因威胁值求和除以10)，计算总染色体个数（将新生代加入set中，可能与历史上出现过的染色体重复）
# 9. 存储三个指标，更新染色体仓库
# 10. 若执行轮次不足100：GOTO 2


start_time = time.time()
# 生成全基因仓库：0-20号
genes_repo = range(21)
# 生成染色体：10条，G0代
ch1 = Chromosome()
genes_list_1 = [20, 1, 2, 10, 17, 12, 4, 5, 9]
ch1.gene_list = genes_list_1
ch1.fitness = 0.95
ch1.total_threat = 3
ch1.ch_name = 'ch1'

ch2 = Chromosome()
genes_list_2 = [18, 2, 8, 19, 5, 14]
ch2.gene_list = genes_list_2
ch2.fitness = 0.8667
ch2.total_threat = 4
ch2.ch_name = 'ch2'

ch3 = Chromosome()
genes_list_3 = [6, 2, 20, 0, 18]
ch3.gene_list = genes_list_3
ch3.fitness = 1.0
ch3.total_threat = 0
ch3.ch_name = 'ch3'

ch4 = Chromosome()
genes_list_4 = [8, 10, 13, 15, 0, 1, 18, 5, 3]
ch4.gene_list = genes_list_4
ch4.fitness = 0.8333
ch4.total_threat = 7
ch4.ch_name = 'ch4'

ch5 = Chromosome()
genes_list_5 = [7, 11, 16, 19, 4, 17, 1]
ch5.gene_list = genes_list_5
ch5.fitness = 0.8
ch5.total_threat = 6
ch5.ch_name = 'ch5'

ch6 = Chromosome()
genes_list_6 = [15, 0, 17, 4, 15, 2, 10]
ch6.gene_list = genes_list_6
ch6.fitness = 0.95
ch6.total_threat = 1
ch6.ch_name = 'ch6'

ch7 = Chromosome()
genes_list_7 = [19, 5, 17, 15, 4, 14, 7, 16]
ch7.gene_list = genes_list_7
ch7.fitness = 0.9167
ch7.total_threat = 3
ch7.ch_name = 'ch7'

ch8 = Chromosome()
genes_list_8 = [0, 10, 9, 5, 20, 8]
ch8.gene_list = genes_list_8
ch8.fitness = 0.9333
ch8.total_threat = 3
ch8.ch_name = 'ch8'

ch9 = Chromosome()
genes_list_9 = [4, 9, 1, 7, 5, 9, 11, 18]
ch9.gene_list = genes_list_9
ch9.fitness = 0.8667
ch9.total_threat = 5
ch9.ch_name = 'ch9'

ch10 = Chromosome()
genes_list_10 = [4, 1, 14, 9, 20]
ch10.gene_list = genes_list_10
ch10.fitness = 0.8833
ch10.total_threat = 6
ch10.ch_name = 'ch10'

ch_total_list = [ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10]
# 计算基因适应度
gene_threat_dict = {}
ch_fitness_total = 0.0
for i in genes_repo:
    gene_threat_dict[i] = 0.0
for ch in ch_total_list:
    l = len(ch.gene_list)
    ch_fitness_total += ch.fitness
    for gene in ch.gene_list:
        t_ge = ch.total_threat / l
        gene_threat_dict[gene] += t_ge
print("基因库威胁值：")
print(gene_threat_dict)
exit(-1)
# 遗传算法
generation_max = 100 # 最大生代
generation_current = 0 # 当前生代
# 统计信息
gene_num_list = [] # 每一生代留存的基因个数
fitness_per_ch_list = [] # 每一生代的平均染色体适应度
ch_num_list = [] # 不重复的染色体个数
ch_repo = set() # 染色体仓库

u = 5 # 每一生代直接留存的染色体个数
n = 5 # 生成新染色体个数
m = 0 # 畸变个数
k = 0 # 当前已生成染色体个数
while k < n:
# for inter in range(n):
    # 选择染色体
    r = random.uniform(0, ch_fitness_total)
    # print("Random = " + str(r))
    choose_ch = 0.0
    chosen_ch_1 = None
    for ch in ch_total_list:
        if choose_ch >= r:
            chosen_ch_1 = ch
            break
        else:
            choose_ch += ch.fitness
    if chosen_ch_1 == None:
        chosen_ch_1 = ch5
    # print("Chosen Ch 1 = " + chosen_ch_1.ch_name)

    r = random.uniform(0, ch_fitness_total)
    # print("Random = " + str(r))
    choose_ch = 0.0
    chosen_ch_2 = None
    for ch in ch_total_list:
        if choose_ch >= r:
            chosen_ch_2 = ch
            break
        else:
            choose_ch += ch.fitness
    if chosen_ch_2 == None:
        chosen_ch_2 = ch5
    # print("Chosen Ch 2 = " + chosen_ch_2.ch_name)

    # 将基因混合，并带上概率
    genes_fitness_dict = {}
    genes_list_choose = []
    total_gene_fitness = 0.0
    for gene in chosen_ch_1.gene_list:
        genes_list_choose.append(gene)
    # 去重
    genes_list_choose = list(set(genes_list_choose))
    # print("选中染色体的基因列表：")
    # print(genes_list_choose)
    for gene in genes_list_choose:
        total_gene_fitness += gene_threat_dict[gene]
    # print("选中染色体的基因总威胁值 = " + str(total_gene_fitness))
    for gene in genes_list_choose:
        genes_fitness_dict[gene] = 1 - gene_threat_dict[gene] / total_gene_fitness
    # print("选中染色体的基因选择概率：")
    # print(genes_fitness_dict)
    gene_fit_total = 0.0
    gene_chosen_next = []
    for gene, fit in genes_fitness_dict.items():
        r = random.random()
        if r < fit:
            gene_chosen_next.append(gene)
    # print("交叉完成后的基因序列：")
    # print(gene_chosen_next)
    # 变异阶段
    stage = 0
    str_m = "增加"
    r = random.randint(0,6)
    if r < 3:
        stage = 0
        str_m = "增加"
    elif r < 5:
        stage = 1
        str_m = "修改"
    else:
        stage = 2
        str_m = "删除"
    pos = random.randint(0, len(gene_chosen_next)-1)
    new_gene = random.choice(genes_repo)
    # print("变异因子：" + str_m + "序列位置：" + str(pos) + "为：" + str(new_gene))
    if stage == 0:
        gene_chosen_next.append(new_gene)
        gene_chosen_next = list(set(gene_chosen_next))
    elif stage == 1:
        gene_chosen_next[pos] = new_gene
    else:
        del gene_chosen_next[pos]
    # print(str_m + "后新基因序列变为:")
    # print(gene_chosen_next)

    # 共存校验
    # if 1 in gene_chosen_next and 12 not in gene_chosen_next:
    #     print("Lose")
    #     m += 1
    #     continue
    # if 8 in gene_chosen_next and 7 not in gene_chosen_next:
    #     print("Lose")
    #     m += 1
    #     continue
    if 13 in gene_chosen_next and 3 in gene_chosen_next:
        print("Lose")
        m += 1
        continue
    if 9 in gene_chosen_next and 5 in gene_chosen_next:
        print("Lose")
        m += 1
        continue
    # 互斥校验
    if 17 in gene_chosen_next and 14 in gene_chosen_next:
        print("Lose")
        m += 1
        continue
    if 14 in gene_chosen_next and 12 in gene_chosen_next:
        print("Lose")
        m += 1
        continue
    if 6 in gene_chosen_next and 13 in gene_chosen_next:
        print("Lose")
        m += 1
        continue
    if 0 in gene_chosen_next and 4 in gene_chosen_next:
        print("Lose")
        m += 1
        continue
    print("success")
    k += 1
print("畸变率：" + str(m/n))
end_time = time.time()
print("GA Cost = " + str(end_time - start_time))