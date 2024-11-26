import pickle
import pickletools

import fastpickle


def test_with_no_shared_ref():
    l = [1, [4, 6, 7], set([0, 9])]
    pickling_order = [0, 1, 2]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_with_simple_shared_list():
    shared_li = [1, 2, 6]
    l = [1, [2, [2, 3], shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_with_simple_shared_list_simple_order():
    shared_li = [1, 2, 6]
    l = [1, [2, [2, 3], shared_li], [3, shared_li]]
    pickling_order = [0, 1, 2]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_four_children():
    shared_li = [1, 2, 6]
    l = [[shared_li, 1], [2, 3, 4, shared_li], [3, 4, 5, shared_li], [4, shared_li]]
    pickling_order = [2, 3, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_shared_set():
    shared_li = set([1, 2, 3])
    l = [[1, shared_li], [2, shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_shared_dict():
    shared_li = {1: [1, 2, 3], 2: 2}
    l = [[[], set([9]), shared_li], [2, shared_li], [3, [], [9, 0], shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_2_shared_li():
    shared_li = [1, 2]
    shared_li2 = [4, 6]
    l = [[shared_li, shared_li2], [2, shared_li], [3, shared_li2, shared_li]]

    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_tuple():
    shared_li = (1, 2, 3)
    l = [[1, shared_li], [2, shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_shared_2_dict():
    shared_li = {1: "hi", 2: "hello", 3: [0, 9, 8]}
    shared_li2 = [6, 7]
    l = [[shared_li, shared_li2], [shared_li2, shared_li]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_shared_2_tuple():
    # In tuples, memoize appears after all the elements
    tuple1 = (1, 2)
    tuple2 = (4, 6)
    l = [[tuple1, tuple2], [1, tuple1]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    print(our_bytecode)
    print(pickle.dumps(l))
    print(pickletools.dis(pickle.dumps(l)))
    assert our_bytecode == pickle.dumps(l)


def test_2():
    shared_li = [1, 2, 3, set([9])]
    l = [[1, [], set([]), shared_li], [2, shared_li], [shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_shared_tuple_with_collections():
    tuple1 = (1, "string")
    l = [[tuple1, 2], [1, tuple1]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_recursive():
    sl = [5, 6]
    sl2 = [4, sl]
    l = [[0, sl2], [1, sl2], [2, [], sl]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_recursive_tuple():
    sl = (5, "hi", 6)
    sl2 = (1, sl)
    l = [[0, sl2], [1, sl2], [2, [], sl]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


class SampleClass:
    def __init__(self, name, values):
        self.name = name
        self.values = values


def test_class():
    obj = SampleClass(name="TestObject", values=[1, 2, 3, [4, 5, 6]])
    l = [obj, [4, 6, 7], set([0, 9])]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_shared_str():
    shared_string = "cs"
    l = [shared_string, [1, shared_string]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_multiple_shared_str():
    shared_string = "cs"
    shared_string2 = "uiuc"
    l = [[shared_string, shared_string2], [1, shared_string, shared_string2]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_long_string():
    long_string = "str" * 10000
    l = [long_string, "short string", [long_string]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_string_with_escape_characters():
    escape_string = "Str1\nStr2\tStr3"
    l = [escape_string, [escape_string, "normal"]]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_two_obj():
    obj = SampleClass(name="TestObject", values=1)
    obj1 = SampleClass(name="TestObject1", values=2)
    l = [obj, [obj, obj1]]
    # l = [obj, [4, 6, 7], set([0, 9])]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_shared_class():
    obj = SampleClass(name="TestObject", values=[1, 2, 3, [4, 5, 6]])
    l = [obj, [4, 6, 7, obj], set([0, 9])]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_two_shared_obj():
    obj = SampleClass(name="TestObject", values=1)
    obj1 = SampleClass(name="TestObject1", values=2)
    l = [[obj1, obj], [obj, obj1]]
    # l = [obj, [4, 6, 7], set([0, 9])]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_many_instances_with_shared_dict():
    shared_dict = {"key1": "a", "key2": "b"}
    obj1 = SampleClass(name="Object1", values=[shared_dict, 123])
    obj2 = SampleClass(name="Object2", values=[shared_dict, 456])
    l = [obj1, obj2, {"key": 789}]
    pickling_order = [2, 0, 1]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_instance_with_mixed_values():
    obj = SampleClass(name="MixedValues", values=[True, "string", 3.14, None, 42])
    l = [obj, 99, "another"]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_nested_class_instances():
    inner_obj = SampleClass(name="InnerObject", values=[1, 2, 3])
    outer_obj = SampleClass(name="OuterObject", values=[inner_obj, 42, "nested"])
    l = [outer_obj, inner_obj]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_class_with_mixed_collections():
    obj = SampleClass(name="MixedCollections", values=[{1, 2}, [3, 4], (5, 6)])
    l = [obj, {"key": {7, 8}}, (9, 10)]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_class_with_large_list_of_values():
    large_list = list(range(500))
    obj = SampleClass(name="LargeList", values=large_list)
    l = [obj, "another"]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_class_with_mutable_immutable_types():
    obj = SampleClass(name="MixedTypes", values=[{"a": 1, "b": 2}, (3, 4), "immutable", 42])
    l = [obj, 99, "another"]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_class_with_simple_self_reference():
    obj = SampleClass(name="SelfReference", values=[42])
    obj.values.append(obj)
    another_value = "another"
    l = [obj, another_value]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_recursive_list():
    l = [1, 2, 3]
    l.append(l)
    pickling_order = [0, 1, 2, 3]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_nested_shared_dict():
    shared_dict_1 = {"a": 1, "b": 2}
    shared_dict_2 = {"x": 10, "y": 20}
    l = [{"dict1": shared_dict_1, "dict2": shared_dict_2}, {"repeat1": shared_dict_1, "repeat2": shared_dict_2}]
    pickling_order = [1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_mixed_nested_structure():
    shared_list = [1, 2, 3]
    shared_set = frozenset([4, 5])
    shared_tuple = (6, 7)
    l = [
        [shared_list, [shared_list, shared_tuple]],
        {shared_set, frozenset(shared_tuple)},
        {"inner_list": shared_list, "inner_set": shared_set, "inner_tuple": shared_tuple},
        {
            "level_2": {
                "shared_list": shared_list,
                "nested_tuple": (shared_tuple, shared_list),
            }
        },
    ]
    pickling_order = [3, 2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_nonlinear_order_with_many_types():
    shared_dict = {"key1": [1, 2], "key2": set([3, 4])}
    shared_tuple = (5, 6)
    l = [
        shared_dict,
        [7, 8, shared_tuple, shared_dict],
        {9, shared_tuple},
        {"nested": [shared_dict, shared_tuple]},
    ]
    pickling_order = [3, 1, 2, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_single_element_collections():
    single_list = [1]
    single_tuple = (1,)
    single_set = {1}
    single_dict = {"key1": 1}
    l = [single_list, single_tuple, single_set, single_dict]
    pickling_order = [3, 2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)


def test_mixed_nested_collections_complex_order():
    complex_list = [1, 2, [3, 4]]
    complex_set = {frozenset({5, 6}), 7}
    complex_tuple = ((8, 9), 10)
    complex_dict = {"key1": complex_list, "key2": complex_list}
    l = [complex_list, complex_set, complex_tuple, complex_dict]
    pickling_order = [1, 0, 2, 3]
    our_bytecode = fastpickle.pardumps(l, pickling_order)
    assert our_bytecode == pickle.dumps(l)
