import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

x_list = range(21)
# gene_list = [21, 19, 20, 18, 19, 20, 18, 19, 12, 13, 18, 16, 11, 15, 18, 12, 16, 16, 15, 14, 14]
gene_list = [21, 19, 19, 20, 18, 15, 18, 17, 16, 10, 16, 15, 18, 16, 13, 17, 16, 13, 11, 13, 18]
fitness_list = [0.90001, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9000000000000001, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.8999999999999998, 0.9, 0.9, 0.9, 0.9]
ch_list = [10, 15, 18, 23, 28, 33, 38, 43, 48, 53, 57, 61, 65, 69, 70, 74, 77, 81, 84, 87, 88]

plt.plot(x_list, gene_list)
plt.xlabel(u"生代")
plt.ylabel(u"包含基因个数")
plt.show()

plt.plot(x_list, fitness_list)
plt.xlabel(u"生代")
plt.ylabel(u"平均适应度")
plt.show()

plt.plot(x_list, ch_list)
plt.xlabel(u"生代")
plt.ylabel(u"多样性集合大小")
plt.show()