import _fastpickle as fp
import _pickle as p


def test_empty():
    lst = []
    fp_dumps = fp.dumps(lst)
    p_dumps = p.dumps(lst)
    fp_out = fp.loads(fp_dumps)
    p_out = p.loads(p_dumps)
    assert fp_out == p_out

def test_ints_simple():
    lst = [1,2,3,4,5,6,7,8,9,10]
    fp_dumps = fp.dumps(lst)
    p_dumps = p.dumps(lst)
    fp_out = fp.loads(fp_dumps)
    p_out = p.loads(p_dumps)
    assert fp_out == p_out

def test_bools_simple():
    lst = [True, False, True, True, False, False]
    fp_dumps = fp.dumps(lst)
    p_dumps = p.dumps(lst)
    fp_out = fp.loads(fp_dumps)
    p_out = p.loads(p_dumps)
    assert fp_out == p_out

def test_strings_simple():
    lst = ['abraca', 'dabra', 'eggg', 'fooo', 'amazing', 'umbrella']
    fp_dumps = fp.dumps(lst)
    p_dumps = p.dumps(lst)
    fp_out = fp.loads(fp_dumps)
    p_out = p.loads(p_dumps)
    assert fp_out == p_out

def test_floats_simple():
    lst =[1.1,2.3,3.1,4.7,5.9,6.2,7.1,8.4,9.9,10.1]
    fp_dumps = fp.dumps(lst)
    p_dumps = p.dumps(lst)
    fp_out = fp.loads(fp_dumps)
    p_out = p.loads(p_dumps)
    assert fp_out == p_out

def test_mixed_simple():
    lst = [1, True, 31, 1, 190 , 10 , 1, 2, 3, 4, 5, 6, 7,8, 9, 10, "1", "2", "3"]
    fp_dumps = fp.dumps(lst)
    p_dumps = p.dumps(lst)
    fp_out = fp.loads(fp_dumps)
    p_out = p.loads(p_dumps)
    assert fp_out == p_out




