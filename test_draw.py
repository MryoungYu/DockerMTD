import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

x_list = range(21)
# gene_list = [21, 19, 20, 18, 19, 20, 18, 19, 12, 13, 18, 16, 11, 15, 18, 12, 16, 16, 15, 14, 14]
gene_list = [21, 19, 19, 20, 18, 15, 18, 17, 16, 10, 16, 15, 18, 16, 13, 17, 16, 13, 11, 13, 18]
fitness_list = [0.8001, 0.8250, 0.8608, 0.8877, 0.9000, 0.8900, 0.9122, 0.9128, 0.92001, 0.92, 0.9201, 0.9220, 0.9267, 0.9296, 0.9308, 0.9291, 0.9333, 0.9340, 0.9355, 0.9356, 0.9380]
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