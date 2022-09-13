class LinkNode:
    def __init__(self, idx, position):
        self.idx = idx
        self.position = position
        self.link_node = []
        self.parent = idx
        
    def add_node(self, road_id):
        self.link_node.append(road_id)
    def parent_node(self, node):
        self.parent = node.idx
    def __eq__(self,other):
        return self.idx == other.idx