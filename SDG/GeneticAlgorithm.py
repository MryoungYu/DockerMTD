class GeneticAlgorithm:
    chromosome_total = []
    genes_repo = []


    def __init__(self, gdgs):

    def exec(self):
        th_new, th_cross= self.select()
        for each_th_cross in th_cross:
            each_th_variation = self.cross(each_th_cross)
            each_th_ga = self.variation(each_th_variation)



