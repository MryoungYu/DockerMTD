from SDG.Node import *
from SDG.Edge import *
class SDG:
    """系统依赖图"""
    node_set = {}
    edge_set = {}
    group_list = []
    type_list = []

    prefix_node_start = '#@node'
    prefix_node_end = '#@end'
    prefix_name = 'name'
    prefix_alias = 'alias'
    prefix_type = 'type'
    prefix_group = 'group'
    prefix_dependence = 'dependence'

    def addNode(self, node):
        self.node_set[node.node_name] = node

    def addEdge(self, edge):
        self.edge_set[edge.edge_name] = edge

    def get_node_by_type(self, type):
        if type not in self.type_list:
            return []
        node_list = []
        for node in self.node_set:
            if node.node_type == type:
                node_list.append(node)
        return node_list

    def get_node_by_group(self, group):
        if group not in self.group_list:
            return []
        node_list = []
        for node in self.node_set:
            if node.node_group == group:
                node_list.append(node)
        return node_list

    def get_edge_by_node(self, node_set):
        edge_set = []


    def generateSDGByDockerfile(self, filepath):
        with open(filepath, 'r') as f:
            list = f.readlines()

        for i in range(0, len(list)):
            line = list[i].rstrip('\n')
            if line.startswith(self.prefix_node_start):
                # 节点开始
                node_name = ''
                node_alias = ''
                node_content = []
                node_type = ''
                node_group = ''
                line = line[6:]
                conf_list = line.split('@')
                for conf in conf_list:
                    if conf == '#' or conf == '':
                        continue
                    content = conf.split('=')[1]
                    if conf.startswith(self.prefix_name):
                        node_name = content
                    if conf.startswith(self.prefix_alias):
                        node_alias = content
                    if conf.startswith(self.prefix_type):
                        node_type = content
                        if node_type not in self.type_list:
                            self.type_list.append(node_type)
                    if conf.startswith(self.prefix_dependence):
                        dependence_list = content.split(',')
                        for dep_item in  dependence_list:
                            dep_info = dep_item.split(':')
                            dep_node_name = dep_info[0]
                            dep_level = dep_info[1]
                            edge_name = "e%d"%(len(self.edge_set)+1)
                            edge = Edge(edge_name, dep_node_name, node_name, dep_level)
                            self.edge_set[edge_name] = edge
                    if conf.startswith(self.prefix_group):
                        node_group = content
                        if node_group not in self.group_list:
                            self.group_list.append(node_group)
            elif line == '#@end':
                node = Node(node_name, node_alias, node_type, node_group, node_content)
                self.node_set[node_name] = node
            else:
                node_content.append(line)

    def change_to_sgdg(self):
        root_node = self.get_node_by_type('Sys')[0]
        # 根据分组信息，提取节点与边，构建分组依赖关系子图
        for group in self.group_list:
            node_set = self.get_node_by_group(group)

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



