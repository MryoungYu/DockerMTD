from graphviz import Digraph

g = Digraph('测试图片')
g.node(name='a',color='red')
g.node(name='b',color='blue')
g.edge('a','b',color='green')
g.view()
