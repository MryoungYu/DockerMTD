class Node:
    node_name = ''
    node_alias = ''
    node_type = ''
    node_group = ''
    node_content = ''

    def __init__(self, name, alias, type, group, content):
        self.node_name = name
        self.node_alias = alias
        self.node_type = type
        self.node_group = group
        self.node_content = content

    def __str__(self):
        str = ''
        str += 'node_name=%s,'%(self.node_name)
        str += 'node_type=%s,'%(self.node_type)
        str += 'node_group=%s,'%(self.node_group)
        str += 'node_content=%s'%(self.node_content)
        return str