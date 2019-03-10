from SDG.Node import *
from SDG.Edge import *
class SDG:
    node_set = {}
    edge_set = {}
    group_list = []
    type_list = []

    def addNode(self, node):
        self.node_set[node.node_name] = node

    def addEdge(self, edge):
        self.edge_set[edge.edge_name] = edge

    def generateSDGByDockerfile(self, filepath):
        with open(filepath, 'r') as f:
            list = f.readlines()
        node_name = ''
        node_content = []
        node_type = ''
        node_group = ''
        for i in range(0, len(list)):
            line = list[i].rstrip('\n')
            if line.startswith('#@node'):
                conf_list = line.split('@')
                for conf in conf_list:
                    if conf == '#':
                        continue
                    content = conf.split('=')[1]
                    if conf.startswith('node='):
                        node_name = content
                    if conf.startswith('type='):
                        node_type = content
                        if node_type not in self.type_list:
                            self.type_list.append(node_type)
                    if conf.startswith('dependence='):
                        dependence_list = content.split(',')
                        for dep_item in  dependence_list:
                            dep_info = dep_item.split(':')
                            dep_node_name = dep_info[0]
                            dep_level = dep_info[1]
                            edge_name = "e%d"%(len(self.edge_set)+1)
                            edge = Edge(edge_name, dep_node_name, node_name, dep_level)
                            self.edge_set[edge_name] = edge
                    if conf.startswith('group='):
                        node_group = content
                        if node_group not in self.group_list:
                            self.group_list.append(node_group)
            elif line == '#@end':
                node = Node(node_name, node_type, node_group, node_content)
                self.node_set[node_name] = node
            else:
                node_content.append(line)

    def __str__(self):
        str = "Node Set:\r\n"
        for k,v in self.node_set.items():
            str += "%s:%s\r\n"%(k, v.__str__())
        str += "Edge Set:\r\n"
        for k,v in self.edge_set.items():
            str += k + ":" + v.__str__() + "\r\n"
        str += "Group List:\r\n"
        str += self.group_list.__str__() + "\r\n"
        str += "Type List:\r\n"
        str += self.type_list.__str__() + "\r\n"
        return str



