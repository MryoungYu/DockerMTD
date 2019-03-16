class GDG:
    """分组依赖图"""
    node_set = {}
    edge_set = {}
    # 组名，组内节点除根节点外，应均不与外部有相连的边
    group_name = ""
    # 根节点，与Sys节点相连
    root_node = None

    def __init__(self, node_set, edge_set, name, root_node):
        self.group_name = name
        self.node_set = node_set
        self.edge_set = edge_set
        self.root_node = root_node