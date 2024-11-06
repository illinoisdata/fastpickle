import _pickle 

class Node:
    def __init__(self, value, nxt):
        self.val = value
        self.nxt = nxt

node1 = Node(1, None)
node2 = Node(2, None)
node3 = Node(3, None)
node1.nxt = node2
node2.nxt = node3
node3.nxt = node3



lst = [node1, node2, node3]
c = _pickle.dumps(lst)
new = _pickle.loads(c)
print(new == lst, new ,lst)