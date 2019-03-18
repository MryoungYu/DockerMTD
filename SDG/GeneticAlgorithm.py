from SDG.Chromosome import *
class GeneticAlgorithm:
    # 染色体库
    chromosome_total = []
    # 基因库
    genes_repo = []
    # 分组名
    group_name = ''
    # 染色体个数
    chromosome_num = 0
    # 当前生代
    current_generation = 0

    def __init__(self, gdgs):
        gene_list = []
        for gdg in gdgs:
            self.group_name = gdg.group_name
            ch = Chromosome(gdg)
            self.chromosome_total.append(ch)
            self.genes_repo += ch.gene_list
        self.genes_repo = list(set(gene_list))

    def exec(self):
        M = 2
        th_new, th_cross= self.select(M)
        th_next_generation = th_new
        for each_th_cross in th_cross:
            each_th_variation = self.cross(each_th_cross)
            each_th_ga = self.variation(each_th_variation)
            if self.check(each_th_ga):
                th_next_generation.append(each_th_ga)




