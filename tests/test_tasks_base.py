import unittest
from unittest.mock import Mock, patch
from cumulusci.core.config.service import ServiceConfig
from cumulusci_jira.tasks import BaseJiraTask


class TestBaseJiraTask(unittest.TestCase):
    @patch("atlassian.Jira")
    @patch("cumulusci_jira.tasks.BaseTask._init_task")
    @patch("cumulusci_jira.tasks.BaseJiraTask._init_jira")
    def setUp(self, mock_init_jira, mock_init_task, mock_jira):
        self.task = BaseJiraTask()
        self.mock_init_jira = mock_init_jira
        self.mock_init_task = mock_init_task
        self.mock_jira = mock_jira

    def test_init_task(self):
        self.task._init_task()
        self.mock_init_task.assert_called_once()
        self.mock_init_jira.assert_called_once()

    @patch("cumulusci_jira.tasks.BaseJiraTask.project_config")
    def test_init_jira(self, mock_project_config):
        mock_service = ServiceConfig(
            {"url": "http://jira.com", "username": "user", "api_token": "token"}
        )
        mock_project_config.keychain.get_service.return_value = mock_service
        self.task._init_jira()
        self.mock_jira.assert_called_once_with(
            url=mock_service.url,
            username=mock_service.username,
            password=mock_service.api_token,
            cloud=True,
        )


if __name__ == "__main__":
    unittest.main()
