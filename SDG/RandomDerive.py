import SDG
import random

class RandomDerive:
    sdgs = []
    group_list = []
    root_list = []

    def __init__(self, sdgs):
        self.sdgs = sdgs
        for sdg in sdgs:
            self.group_list += sdgs
            self.root_list += sdg.get_node_by_type('Sys')

    def exec(self):
        r = random.randint()