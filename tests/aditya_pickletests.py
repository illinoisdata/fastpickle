import _pickle as p
from collections import deque

def test_dumps():


    spec = [[1,2,3]]
    chars = ["a", "b", "c"]
    shared = 99
    ints = [1,shared, 2,3,shared, 14]
    bools = [False, True,False]
    mixed = [1,bools,31, chars, spec, 1, 190 , 10 , 1, 2, 3, 4, 5, 6, 7,8, 9, 10, "1", "2", "3"]
    longlist = [i for i in range(10000)]
    # [a,b,c]
    lst = mixed

    # q = deque([])
    # q.append("a")

    
    try:        
        # print(f"{i}")
        out = p.dumps(lst)
        # print(f"serialized_output:'{out}'")
    except Exception as e:
        print("Exception occurred during loop:", e)
    # out = p.dumps(lst)
    print(p.loads(out) == lst)
    print(p.loads(out))

if __name__ == "__main__":
    test_dumps()




# # the class below would invoke the memoization function..not there yet
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.next = None
#     def AddNext(self, node):
#         self.next = node