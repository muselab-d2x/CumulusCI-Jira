from cumulusci.core.exceptions import CumulusCIFailure


class JiraIssueNotFound(CumulusCIFailure):
    """Raised when a Jira issue is not found"""

    def __init__(self, issue_key):
        super().__init__(f"Jira issue {issue_key} not found")
