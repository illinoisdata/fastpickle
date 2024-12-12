import pickle
import pickletools
import gc
import fastpickle


def test_with_no_shared_ref():
    l = [1, [4, 6, 7], set([0, 9])]
    pickling_order = [0, 1, 2]
    our_bytecode = fastpickle.dumps(l)
    


def test_with_simple_shared_list():
    shared_li = [1, 2, 6]
    l = [1, [2, [2, 3], shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_with_simple_shared_list_simple_order():
    shared_li = [1, 2, 6]
    l = [1, [2, [2, 3], shared_li], [3, shared_li]]
    pickling_order = [0, 1, 2]
    our_bytecode = fastpickle.dumps(l)
    


def test_four_children():
    shared_li = [1, 2, 6]
    l = [[shared_li, 1], [2, 3, 4, shared_li], [3, 4, 5, shared_li], [4, shared_li]]
    pickling_order = [2, 3, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_shared_set():
    shared_li = set([1, 2, 3])
    l = [[1, shared_li], [2, shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
     


def test_shared_dict():
    shared_li = {1: [1, 2, 3], 2: 2}
    l = [[[], set([9]), shared_li], [2, shared_li], [3, [], [9, 0], shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_2_shared_li():
    shared_li = [1, 2]
    shared_li2 = [4, 6]
    l = [[shared_li, shared_li2], [2, shared_li], [3, shared_li2, shared_li]]

    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_tuple():
    shared_li = (1, 2, 3)
    l = [[1, shared_li], [2, shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_shared_2_dict():
    # gc.disable()
    shared_li = {1: "hi", 2: "hello", 3: [0, 9, 8]}
    shared_li2 = [6, 7]
    l = [[shared_li, shared_li2], [shared_li2, shared_li]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_shared_2_tuple():
    # In tuples, memoize appears after all the elements
    tuple1 = (1, 2)
    tuple2 = (4, 6)
    l = [[tuple1, tuple2], [1, tuple1]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.dumps(l)
    print(our_bytecode)
    print(pickle.dumps(l))
    print(pickletools.dis(pickle.dumps(l)))
    


def test_2():
    shared_li = [1, 2, 3, set([9])]
    l = [[1, [], set([]), shared_li], [2, shared_li], [shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_shared_tuple_with_collections():
    tuple1 = (1, "string")
    l = [[tuple1, 2], [1, tuple1]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_recursive():
    sl = [5, 6]
    sl2 = [4, sl]
    l = [[0, sl2], [1, sl2], [2, [], sl]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_recursive_tuple():
    sl = (5, "hi", 6)
    sl2 = (1, sl)
    l = [[0, sl2], [1, sl2], [2, [], sl]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


class SampleClass:
    def __init__(self, name, values):
        self.name = name
        self.values = values


def test_class():
    obj = SampleClass(name="TestObject", values=[1, 2, 3, [4, 5, 6]])
    l = [obj, [4, 6, 7], set([0, 9])]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_shared_str():
    shared_string = "cs"
    l = [shared_string, [1, shared_string]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_multiple_shared_str():
    shared_string = "cs"
    shared_string2 = "uiuc"
    l = [[shared_string, shared_string2], [1, shared_string, shared_string2]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_two_obj():
    obj = SampleClass(name="TestObject", values=1)
    obj1 = SampleClass(name="TestObject1", values=2)
    l = [obj, [obj, obj1]]
    # l = [obj, [4, 6, 7], set([0, 9])]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_shared_class():
    obj = SampleClass(name="TestObject", values=[1, 2, 3, [4, 5, 6]])
    l = [obj, [4, 6, 7, obj], set([0, 9])]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.dumps(l)
    


def test_two_shared_obj():
    obj = SampleClass(name="TestObject", values=1)
    obj1 = SampleClass(name="TestObject1", values=2)
    l = [[obj1, obj], [obj, obj1]]
    # l = [obj, [4, 6, 7], set([0, 9])]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.dumps(l)
    
