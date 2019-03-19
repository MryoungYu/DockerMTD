class SGDG:
    """系统依赖图的分组表示方法"""
    root_node = None
    group_list = []
    gdg_dict = {}

    def __init__(self, root, gdgs):
        self.root_node = root
        self.group_list = list()
        self.gdg_dict = dict()
        for gdg_group, gdg in gdgs.items():
            self.group_list.append(gdg.group_name)
            self.gdg_dict[gdg.group_name] = gdg
