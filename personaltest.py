import _pickle as p

# the function below would invoke the memoization function
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
    def AddNext(self, node):
        self.next = node
    
# works for longs, floats?
# fails for strings, 
def test_dumps():

    node1 = Node(2)
    node2 = Node(3)
    node3 = Node(4)


#singletons work, fails after that
    nodes = [node1, node2]
    spec1 = [[node1]]
    spec = [[1,2,3]]
    chars = ["a", "b", "c"]
    shared = 99
    ints = [1,shared, 2,3,4, 14]
    bools = [False, True,False]
    mixed = [1,23,31, 23, 111, 1]
    # [a,b,c]
    lst = bools

    try:
        out = p.dumps(lst)
        print("Serialized Output: ", out)
        deserialized_lst = p.loads(out)
        print("Deserialized Output: ", deserialized_lst)
        print(lst == deserialized_lst)
    except Exception as e:
        print("Exception occurred:", e)

if __name__ == "__main__":
    test_dumps()
