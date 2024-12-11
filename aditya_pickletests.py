import _fastpickle as p
import time
import gc

def test_dumps():
    spec = [[1,2,"a", "b", 3]]
    chars = ["a", "b", "c", "d", "e"]
    # shared = 99
    # ints = [1,shared, 2,3,shared, 14]
    bools = [False, True,False]
    mixed = [1, True, 31, 1, 190 , 10 , 1, 2, 3, 4, 5, 6, 7,8, 9, 10, "1", "2", "3"]
    longlist = [i for i in range(1000)]
    # [a,b,c]
    ints_simple = [1,2,3,4,5,6,7,8,9,10]
    lst = spec  

    # q = deque([])
    # q.append("a")   
    res = 0.0
    out = ""
    try:        
        # print(f"{i}")
        res = time.time()
        # gc.disable()  # Disable garbage collection
        # gc.set_threshold(0)
        out = p.dumps(lst)
        # print(f"serialized_output:'{out}'")
        res = time.time()-res
    except Exception as e:
        print("Exception occurred during loop:", e)
        res = -1.0
    # print(out)
    # print(p.loads(out) == lst)
    if p.loads(out) != lst:
        res = -1.0
    # print(p.loads(out))
    return res

if __name__ == "__main__":
    print(p.__file__)
    # for _ in range(100):
    #     test_dumps()
    val = 0.0
    count = 1
    for i in range(count):
        result = test_dumps()
        if result==-1.0:
            print(f"res was -1 for {i}")
            break
        else:
            val += result
    print(val/count)


