from SDG.Chromosome import *
import random
import time
start_time = time.time()

genes_repo = range(21)

ch1 = Chromosome()
genes_list_1 = [20, 1, 2, 10, 17, 12, 4, 5, 9]
ch1.gene_list = genes_list_1
ch1.fitness = 0.8053
ch1.total_threat = 13
ch1.ch_name = 'ch1'

ch2 = Chromosome()
genes_list_2 = [18, 2, 8, 19, 5, 14]
ch2.gene_list = genes_list_2
ch2.fitness = 0.7884
ch2.total_threat = 12
ch2.ch_name = 'ch2'

ch3 = Chromosome()
genes_list_3 = [6, 2, 20, 0, 18]
ch3.gene_list = genes_list_3
ch3.fitness = 0.8628
ch3.total_threat = 9
ch3.ch_name = 'ch3'

ch4 = Chromosome()
genes_list_4 = [8, 10, 13, 15, 0, 1, 18, 5, 3]
ch4.gene_list = genes_list_4
ch4.fitness = 0.7789
ch4.total_threat = 14
ch4.ch_name = 'ch4'

ch5 = Chromosome()
genes_list_5 = [7, 11, 16, 19, 4, 17, 1]
ch5.gene_list = genes_list_5
ch5.fitness = 0.8648
ch5.total_threat = 10
ch5.ch_name = 'ch5'

ch_total_list = [ch1, ch2, ch3, ch4, ch5]
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
n = 20
m = 0
k = 0
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