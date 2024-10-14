import pickle
import pytest
import fastpickle

def test_with_no_shared_ref():
    l = [1, [4, 6, 7], set([0, 9])]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order)  
    assert our_bytecode == pickle.dumps(l)

def test_with_simple_shared_list():
    shared_li = [1, 2, 6]
    l = [1, [2, [2, 3], shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
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
    shared_li = {1:[1, 2, 3], 2:2}
    l = [[shared_li], [2, shared_li], [3, shared_li]]
    pickling_order = [2, 1, 0]
    our_bytecode = fastpickle.pardumps(l, pickling_order) 
    assert our_bytecode == pickle.dumps(l)
