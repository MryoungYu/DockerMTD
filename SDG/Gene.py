class Gene:
    node_set = {}
    edge_set = {}
    group_name = ''
    node_num = 0

    def create_gene_by_node(self, node):
        self.node_set[node.node_name] = node
        node_num = 1
        self.group_name = node.node_group

    def create_gene_by_MDU(self, node_list, edge_list):
        self.group_name = node_list[0].node_group
        for node in node_list:
            self.node_set[node.node_name] = node
        for edge in edge_list:
            self.edge_set[edge.edge_name] = edge
        self.node_num = len(node_list)

    def __eq__(self, other):
        if self.node_set == other.node_set and self.edge_set == other.edge_set \
                and self.group_name == other.group_name and self.node_num == other.node_num:
            return True
        else:
            return False