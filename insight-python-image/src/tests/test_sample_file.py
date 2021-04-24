import os
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)
from sample_file import add
from sample_file import minus


def test_add():
    actual = add(1, 2)
    expected = 3
    assert expected == actual

def test_minus():
    actual = minus(3, 2)
    expected = 1
    assert expected == actual
