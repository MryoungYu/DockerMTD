class BAG:
    # 节点个数，除起始点外
    node_num = 8
    # 一步转移概率矩阵
    trans_prob = [
        #P*0   P*1   P*2   P*3   P*4   P*5   P*6   P*7   P*8
        [1.,   0.69, 0.54, 0.,   0.54, 0.,   0.,   0.,   0.  ], # P0*
        [0.,   1.,   0.,   0.,   0.,   0.45, 0.69, 0.,   0.  ], # P1*
        [0.,   0.,   1.,   0.45, 0.,   0.,   0.69, 0.,   0.  ], # P2*
        [0.,   0.,   0.,   1.,   0.,   0.,   0.69, 0.,   0.  ], # P3*
        [0.,   0.,   0.,   0.45, 1.,   0.,   0.69, 0.,   0.  ], # P4*
        [0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,   0.69], # P5*
        [0.,   0.,   0.,   0.,   0.,   0.45, 1.,   0.69, 0.69], # P6*
        [0.,   0.,   0.,   0.,   0.,   0.45, 0.,   1.,   0.69], # P7*
        [0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.  ], # P8*
    ]
    # 实时可达概率
    access_prob = []
    # 节点价值
    loss_value = [0, 8.3, 3.8, 3.8, 3.8, 11.1, 11.1, 11.1, 12.2]
    # 资产价值
    asset_value = [2, 4, 4, 4, 3, 3, 3, 5]
    # 威胁值
    node_threat = []
    # 攻击者的经验加成比例
    attacker_experience = 1.2

    def __init__(self):
        # TODO 可以从文件中读取信息计算trans_prob和loss_value
        # for test
        self.node_num = 3
        self.trans_prob = [
            [0.1, 0.5, 0.4, 0.],
            [0., 0.8, 0., 0.2],
            [0., 0., 0.3, 0.7],
            [0., 0., 0., 1.],
        ]
        self.loss_value = [0, 1, 2, 3]
        # test end
        self.access_prob = self.cal_access_pro()
        self.node_threat = self.cal_node_threat()


    def cal_access_pro(self):
        """计算节点的可达概率"""
        access_pro_list = []
        return access_pro_list;

    def cal_node_threat(self):
        """计算每个节点的威胁值"""
        threat_list = []
        return threat_list

    def cal_system_threat(self):
        """计算整体威胁值"""
        total_threat = 0.0
        total_asset_value = 0.0
        for i in range(len(self.node_threat)):
            total_threat += self.node_threat[i] * self.asset_value[i]
            total_asset_value += self.asset_value[i]
        return total_threat / total_asset_value

    def update_trans_prob(self, attack_path):
        for i in attack_path:
            for j in range(self.node_num + 1):
                self.trans_prob[i][j] *= self.attacker_experience
