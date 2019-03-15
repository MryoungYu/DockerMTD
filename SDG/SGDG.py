class SGDG:
    """系统依赖图的分组表示方法"""
    root_node = False
    gdg_list = []

    def __init__(self, root, gdgs):
        self.root_node = root
        self.gdg_list = gdgs