

from parameterized import parameterized_class
from fixtures import TEST_PAYLOAD


import unittest
from unittest.mock import patch
from client import GithubOrgClient

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
    for org_payload, repos_payload, expected_repos, apache2_repos in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks for requests.get"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url == cls.org_payload["repos_url"]:
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            return unittest.mock.DEFAULT

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

