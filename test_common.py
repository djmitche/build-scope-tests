"""
Tests for the common functions.
"""

from nose.tools import eq_
import common

def test_flatten():
    eq_(common._flatten(['a', 'b']), ['a', 'b'])

def test_flatten_nested():
    eq_(common._flatten(['a', ['b', 'c']]), ['a', 'b', 'c'])

def test_flatten_nested_deeply():
    eq_(common._flatten([['a'], [[['b', 'c']]]]), ['a', 'b', 'c'])
