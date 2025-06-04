#!/usr/bin/env python3
"""Test suite for access_nested_map function.
"""
from parameterized import parameterized
import unittest
from utils import access_nested_map 


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand ([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])

    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map (nested_map, path), expected)




class TestAccessNestedMapExceptions(unittest.TestCase):
    @parameterized.expand ([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])

    def test_access_nested_map_exceptions(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


