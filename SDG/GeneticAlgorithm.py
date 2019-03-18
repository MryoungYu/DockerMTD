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
        self.chromosome_num = len(gdgs)
        for gdg in gdgs:
            self.group_name = gdg.group_name
            ch = Chromosome(gdg)
            self.chromosome_total.append(ch)
            self.genes_repo += ch.gene_list
        self.genes_repo = list(set(gene_list))

    def exec(self):
        # 直接进入下一生代的染色体个数
        M = 2
        # 选择算子-1
        th_new = self.select_next(M)
        th_next_generation = th_new
        while len(th_next_generation) < self.chromosome_num:
            # 选择算子-2
            th_cross_1, th_cross_2 = self.select_croos()
            # 交叉算子
            th_variation = self.cross(th_cross_1, th_cross_2)
            # 变异算子
            th_ga = self.variation(th_variation)
            # 后置检查
            if self.check(th_ga):
                th_next_generation.append(th_ga)
        # 生代加1
        self.current_generation += 1
        return th_next_generation

    def select_next(self, M):
        """选择直接进入下一生代的Top M个染色体"""

    def select_cross(self):
        """以概率的方式选择两个染色体进入交叉算子"""

    def cross(self, th1, th2):
        """交叉算子"""

    def variation(self, th):
        """变异算子"""

    def check(self, th):
        """后置检查"""
        return True