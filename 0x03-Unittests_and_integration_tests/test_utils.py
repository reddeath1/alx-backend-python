import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock
from client import GithubOrgClient
from urllib.error import HTTPError
from fixtures import TEST_PAYLOAD

class TestGithubOrgClient(unittest.TestCase):
    @patch('client.get_json')
    def test_org(self, mocked_get_json):
        mocked_get_json.return_value = {'login': 'test_org'}
        gh_org_client = GithubOrgClient('test_org')
        self.assertEqual(gh_org_client.org, {'login': 'test_org'})
        mocked_get_json.assert_called_once_with('https://api.github.com/orgs/test_org')

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mocked_org):
        mocked_org.return_value = {'repos_url': 'https://api.github.com/orgs/google/repos'}
        gh_org_client = GithubOrgClient('google')
        self.assertEqual(gh_org_client._public_repos_url, 'https://api.github.com/orgs/google/repos')

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mocked_public_repos_url, mocked_get_json):
        mocked_public_repos_url.return_value = 'https://api.github.com/orgs/google/repos'
        mocked_get_json.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]
        gh_org_client = GithubOrgClient('google')
        self.assertEqual(gh_org_client.public_repos(), ['repo1', 'repo2'])
        mocked_public_repos_url.assert_called_once()
        mocked_get_json.assert_called_once()

    @patch('client.get_json')
    def test_has_license(self, mocked_get_json):
        gh_org_client = GithubOrgClient('google')
        mocked_get_json.return_value = {'license': {'key': 'bsd-3-clause'}}
        self.assertTrue(gh_org_client.has_license({}, 'bsd-3-clause'))
        mocked_get_json.assert_called_once_with('https://api.github.com/orgs/google')

class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def mock_get_payload(url):
            payload_map = {
                'https://api.github.com/orgs/google': TEST_PAYLOAD[0][0],
                'https://api.github.com/orgs/google/repos': TEST_PAYLOAD[0][1]
            }
            if url in payload_map:
                return Mock(json=Mock(return_value=payload_map[url]))
            raise HTTPError
        cls.patcher = patch('requests.get', side_effect=mock_get_payload)
        cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def test_public_repos(self):
        gh_org_client = GithubOrgClient('google')
        self.assertEqual(gh_org_client.public_repos(), TEST_PAYLOAD[0][2])

    def test_public_repos_with_license(self):
        gh_org_client = GithubOrgClient('google')
        self.assertEqual(gh_org_client.public_repos(license='apache-2.0'), TEST_PAYLOAD[0][3])

if __name__ == '__main__':
    unittest.main()
