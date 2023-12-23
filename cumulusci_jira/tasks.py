import re
from atlassian import Jira
from cumulusci.core.exceptions import TaskOptionsError
from cumulusci.core.tasks import BaseTask
from cumulusci_jira.exceptions import JiraIssueNotFound


class BaseJiraTask(BaseTask):
    def _init_task(self):
        super()._init_task()
        self._init_jira()

    def _init_jira(self):
        service = self.project_config.keychain.get_service("jira")
        self.jira = Jira(
            url=service["url"],
            username=service["username"],
            password=service["api_token"],
            cloud=True,
        )


ISSUE_KEY_REGEX = r"^[A-Z][A-Z0-9]{1,9}$"
PROJECT_KEY_REGEX = r"^[A-Z][A-Z0-9]{1,9}$"


class BaseJiraProjectTask(BaseJiraTask):
    task_options = {
        "project": {
            "description": "The Jira project key",
            "required": True,
        },
    }

    def _validate_options(self):
        super()._validate_options()
        # Check that the project key is a valid Jira project key using regex
        if not re.match(PROJECT_KEY_REGEX, self.options["project"]):
            raise TaskOptionsError(
                f"Project key {self.options['project']} is not a valid Jira project key"
            )


class BaseJiraIssueTask(BaseJiraTask):
    task_options = {
        "issue": {
            "description": "The Jira issue key",
            "required": True,
        },
    }

    def _validate_options(self):
        super()._validate_options()
        # Check that the issue key is a valid Jira issue key using regex
        if not re.match(ISSUE_KEY_REGEX, self.options["issue"]):
            raise TaskOptionsError(
                f"Issue key {self.options['issue']} is not a valid Jira issue key"
            )
        if not self.get_issue():
            raise JiraIssueNotFound(self.options["issue"])

    def get_issue(self):
        return self.jira.issue(self.options["issue"])
