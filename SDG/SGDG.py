import Edge
import SDG
class SGDG:
    """系统依赖图的分组表示方法"""
    root_node = None
    group_list = []
    gdg_dict = {}

    def __init__(self, root, gdgs):
        self.root_node = root
        for gdg in gdgs:
            self.group_list.append(gdg.group_name)
            self.gdg_dict[gdg.group_name] = gdg

    def change_to_sdg(self):
        """解除GDG形式，恢复成SDG形式"""
        sdg_group_list = self.group_list
        sdg_node_list = [self.root_node]
        sdg_edge_list = []
        for group in self.group_list:
            gdg_list = self.gdg_dict[group]
            for gdg in gdg_list:
                sdg_node_list += gdg.node_set
                sdg_edge_list += gdg.edge_set
                e = Edge('root_' + group,self.root_node, gdg.root_node, 1)
                sdg_edge_list.append(e)
        sdg = SDG(sdg_node_list, sdg_edge_list, sdg_group_list, ['Sys', 'App', 'Conf', 'Inter')
        return sdg