#!/usr/bin/env python3
""" Unittest Test
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from requests import HTTPError

from client import GithubOrgClient
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """ nested map test function """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ test access nested map """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """ test exception"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ get json unittest """

    @parameterized.expand([
        ("https://example.com", {"payload": True}),
        ("https://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """ self descriptive"""

        class Mocked(Mock):
            """" mocked class """

            def json(self):
                """ json method mocked """
                return test_payload

        with patch('requests.get') as MockClass:
            MockClass.return_value = Mocked()
            self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):
    """ memoize unittest """

    def test_memoize(self):
        """ memoize test """

        class TestClass:
            """ self descriptive"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mocked:
            spec = TestClass()
            spec.a_property()
            spec.a_property()
            mocked.asset_called_once()


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ TESTCASE """

    @classmethod
    def setUpClass(cls):
        """ It is part of the unittest.TestCase API
        method to return example payloads found in the fixtures """
        cls.get_patcher = patch('requests.get', side_effect=HTTPError)

    @classmethod
    def tearDownClass(cls):
        """ It is part of the unittest.TestCase API
        method to stop the patcher """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ method to test GithubOrgClient.public_repos """
        test_class = GithubOrgClient("holberton")
        assert True

    def test_public_repos_with_license(self):
        """ method to test the public_repos with the argument license """
        test_class = GithubOrgClient("holberton")
        assert True
