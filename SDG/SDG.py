from SDG.Node import Node
from SDG.Edge import Edge
from SDG.GDG import GDG
from SDG.SGDG import SGDG
from graphviz import Digraph

class SDG:
    """系统依赖图"""
    SDG_name = ''
    node_set = {}
    edge_set = {}
    group_list = []
    type_list = []

    node_shape = {
        'Sys':'parallelogram',
        'App':'diamond',
        'Conf':'box',
        'Inter':'circle',
    }

    prefix_node_start = '#@node'
    prefix_node_end = '#@end'
    prefix_name = 'name'
    prefix_alias = 'alias'
    prefix_type = 'type'
    prefix_group = 'group'
    prefix_dependence = 'dependence'

    def __init__(self):
        self.node_set = dict()
        self.edge_set = dict()
        self.group_list = list()
        self.type_list = list()

    def set_SDG(self, node_set, edge_set, group_list, type_list):
        self.node_set = node_set
        self.edge_set = edge_set
        self.group_list = group_list
        self.type_list = type_list

    def addNode(self, node):
        self.node_set[node.node_name] = node

    def addEdge(self, edge):
        self.edge_set[edge.edge_name] = edge

    def get_node_by_type(self, type):
        if type not in self.type_list:
            return []
        node_list = []
        for node_name, node in self.node_set.items():
            if node.node_type == type:
                node_list.append(node)
        return node_list

    def get_node_by_group(self, group):
        if group not in self.group_list:
            return []
        node_list = []
        for node_name, node in self.node_set.items():
            if node.node_group == group:
                node_list.append(node)
        return node_list

    def get_edge_by_node(self, node_set):
        edge_set = []
        node_name_set = []
        for node in node_set:
            node_name_set.append(node.node_name)
        for edge_name, edge in self.edge_set.items():
            if edge.edge_start_node in node_name_set and edge.edge_end_node in node_name_set:
                edge_set.append(edge)
        return edge_set

    def draw_graph(self):
        g = Digraph(self.SDG_name)
        for node_name, node in self.node_set.items():
            if node.node_alias != '':
                node_label = node.node_alias
            else:
                node_label = node.node_name
            g.node(name=node_name, label=node_label, shape=self.node_shape[node.node_type])
        for edge_name, edge in self.edge_set.items():
            g.edge(edge.edge_start_node, edge.edge_end_node, edge_name)
        print(g.source)
        g.render('SDG-output/' + self.SDG_name + '.gv', view=False)

    # def generate_dockerfile(self, filepath):
    #     with open(filepath, 'w') as f:
    #

    def generateSDGByDockerfile(self, filepath):
        filename = filepath.split('/')
        self.SDG_name = filename[len(filename)-1]
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

    def generate_by_SGDG(self, sgdg):
        """解除GDG形式，恢复成SDG形式"""
        sdg_group_list = sgdg.group_list
        sdg_node_list = [sgdg.root_node]
        sdg_edge_list = []
        for group in sgdg.group_list:
            gdg = sgdg.gdg_dict[group]
            sdg_node_list += gdg.node_set
            sdg_edge_list += gdg.edge_set
            e = Edge('root_' + group, sgdg.root_node.node_name, gdg.root_node, 1)
            sdg_edge_list.append(e)
        for node in sdg_node_list:
            self.node_set[node.node_name] = node
        for edge in sdg_edge_list:
            self.edge_set[edge.edge_name] = edge
        self.group_list = sdg_group_list
        self.type_list = ['Sys', 'App', 'Conf', 'Inter']

    def change_to_sgdg(self):
        root_node = self.get_node_by_type('Sys')[0]
        gdg_dict = {}
        # 根据分组信息，提取节点与边，构建分组依赖关系子图
        for group in self.group_list:
            node_set = self.get_node_by_group(group)
            edge_set = self.get_edge_by_node(node_set)
            node_name_list = []
            gdg_root_node = None
            for node in node_set:
                node_name_list.append(node.node_name)
            for edge_name, edge in self.edge_set.items():
                if edge.edge_start_node == root_node.node_name and edge.edge_end_node in node_name_list:
                    gdg_root_node = edge.edge_end_node
                    break
            gdg = GDG(node_set, edge_set, group, gdg_root_node)
            gdg_dict[group] = gdg
        sgdg = SGDG(root_node, gdg_dict)
        return sgdg

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



