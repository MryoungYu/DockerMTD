from SDG.Gene import *
class Chromosome:
    # 基因序列
    gene_list = []
    # 适应度
    fitness = 0

    def __init__(self, gdg):
        """基因提取算法"""
        gene_list = []
        # 根据依赖强度拆分MDU与单节点基因
        node_set_list = []
        edge_set_list = []
        for edge_name, edge in gdg.edge_set:
            if edge.edge_dependence >= 3:
                start_node = edge.edge_start_node
                end_node = edge.edge_end_node
                index = -1
                for node_list in node_set_list:
                    if start_node in node_list or end_node in node_list:
                        node_list.append(start_node)
                        node_list.append(end_node)
                        index = node_set_list.index(node_list)
                        break
                if index != -1:
                    # 已存在MDU
                    edge_set_list[index].append(edge)
                else:
                    # 新建MDU
                    node_list = [start_node, end_node]
                    node_set_list.append(node_list)
                    edge_list = [edge]
                    edge_set_list.append(edge_list)
        # 遍历MDU生成基因
        exist_node_list = []
        for i in range(len(node_set_list)):
            node_list = node_set_list[i]
            exist_node_list += node_list
            edge_list = edge_set_list[i]
            gene = Gene()
            gene.create_gene_by_MDU(node_list, edge_list)
            gene_list.append(gene)
        # 遍历其他节点生成单节点基因
        for node_name, node in gdg.node_set.items():
            if node not in exist_node_list:
                gene = Gene()
                gene.create_gene_by_node(node)
                gene_list.append(gene)
        self.gene_list = gene_list