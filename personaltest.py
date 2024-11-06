import _pickle as p

# the function below would invoke the memoization function
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.next = None
#     def AddNext(self, node):
#         self.next = node
    
# works for longs, floats?
# fails for strings, 
def test_dumps():


    a = 11
    b = 20
    e = 2
    f = 3
    g = 4
    h = 5
 
    c = a
    shared = b

    lst = [a, b, c, e, f, g, h]
    lst2 = [shared, a, a, a, a, a, c]

    try:
        out = p.dumps(lst)
        out2 = p.dumps(lst2)
        print("Serialized Output: ", out)
        print("Serialized Output: ", out2)
        deserialized = p.loads(out)
        deserialized2= p.loads(out2)
        print("Deserialized Output:", deserialized)
        print("Deserialized Output:", deserialized2)
    except Exception as e:
        print("Exception occurred:", e)

if __name__ == "__main__":
    test_dumps()
