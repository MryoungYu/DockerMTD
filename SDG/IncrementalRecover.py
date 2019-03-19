from SDG.Edge import *
class IncrementalRecover:
    recover_condition = None
    recover_node = None
    sdg = None

    def __init__(self, sdg, recover_condition, recover_node):
        self.sdg = sdg
        self.recover_condition = recover_condition
        self.recover_node = recover_node

    def exec(self):
        # 检查是否满足修复条件
        for node_name, node in self.sdg.node_set.items():
            if node == self.recover_condition:
                self.sdg.node_set[self.recover_node.node_name] = self.recover_node
                for edge_name, edge in self.sdg.edge_set.items():
                    if edge.edge_start_node == node_name:
                        edge.edge_start_node = self.recover_node.node_name
                recover_edge = Edge('recover_' + node.node_name, node_name, self.recover_node.node_name, 3)
                self.sdg.edge_set[recover_edge.edge_name] = recover_edge
                return True
        return False


