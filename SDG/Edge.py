class Edge:
    edge_name = ''
    edge_start_node = False
    edge_end_node = False
    edge_dependence = 0

    def __init__(self, name, start_node, end_node, dependence):
        self.edge_name = name
        self.edge_start_node = start_node
        self.edge_end_node = end_node
        self.edge_dependence = dependence

    def __str__(self):
        str = ""
        str += "edge_name=%s,"%(self.edge_name)
        str += "edge_start_node=%s,"%(self.edge_start_node)
        str += "edge_end_node=%s,"%(self.edge_end_node)
        str += "edge_dependence=%s"%(self.edge_dependence)
        return str
