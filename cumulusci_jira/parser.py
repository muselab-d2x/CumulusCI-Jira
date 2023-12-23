import logging
import re
import urllib.parse

from atlassian import Jira

from cumulusci.core.versions import PackageVersionNumber
from cumulusci.tasks.release_notes.parser import IssuesParser
from .exceptions import JiraIssueNotFound


class JiraIssuesParser(IssuesParser):
    ISSUE_COMMENT = {
        "beta": "Included in beta release",
        "prod": "Included in production release",
    }

    def __new__(cls, release_notes_generator, title, issue_regex=None):
        if not release_notes_generator.has_issues:
            logging.getLogger(__file__).warn("Issues are disabled for this repository.")

        return super().__new__(cls)

    def __init__(self, release_notes_generator, title, issue_regex=None):
        super().__init__(release_notes_generator, title, issue_regex)
        self.link_pr = release_notes_generator.link_pr
        self.pr_number = None
        self.pr_url = None
        self.publish = release_notes_generator.do_publish
        service = self.release_notes_generator.project_config.keychain.get_service("jira")
        self.jira = Jira(
            url=service.url,
            username=service.username,
            password=service.api_token,
            cloud=True,
        )

    def _get_default_regex(self):
        return r"\b([A-Z]{2,10})-(\d+)\b"

    def _add_line(self, line):
        # find issue numbers per line
        matches = re.match(self.issue_regex, line, flags=re.IGNORECASE)
        for match in matches:
            issue_key = match.group(0)
            issue_number = match.group(2)
            self.content.append(
                {
                    "issue_number": int(issue_number),
                    "issue_key": int(issue_key),
                    "pr_number": self.pr_number,
                    "pr_url": self.pr_url,
                }
            )

    def _get_default_regex(self):
        keywords = (
            "close",
            "closes",
            "closed",
            "fix",
            "fixes",
            "fixed",
            "resolve",
            "resolves",
            "resolved",
        )
        return r"(?:{})\s\[?#(\d+)\]?".format("|".join(keywords))

    def _render_content(self):
        content = []
        for item in sorted(self.content, key=lambda k: k["issue_number"]):
            issue = self._get_issue(item["issue_key"])
            txt = f"#{issue.key}: {issue.title}"
            if self.link_pr:
                txt += " [[PR{}]({})]".format(item["pr_number"], item["pr_url"])
            content.append(txt)
            if self.publish:
                self._add_issue_comment(issue)
        return "\r\n".join(content)

    def _get_issue(self, issue_key):
        try:
            issue = self.jira.issue(issue_key)
        except Exception as exc:
            raise JiraIssueNotFound(issue_key) from exc
        return issue

    def _process_change_note(self, pull_request):
        self.pr_number = pull_request.number
        self.pr_url = pull_request.html_url
        return pull_request.body

    def _add_issue_comment(self, issue):
        # Ensure all issues have a comment on which release they were fixed
        prefix_beta = self.release_notes_generator.github_info["prefix_beta"]
        prefix_prod = self.release_notes_generator.github_info["prefix_prod"]

        # ParentPullRequestNotesGenerator doesn't utilize a current_tag
        if not hasattr(self.release_notes_generator, "current_tag"):
            return
        elif self.release_notes_generator.current_tag.startswith(prefix_beta):
            is_beta = True
        elif self.release_notes_generator.current_tag.startswith(prefix_prod):
            is_beta = False
        else:
            # not production or beta tag, don't comment
            return
        if is_beta:
            comment_prefix = self.ISSUE_COMMENT["beta"]
        else:
            comment_prefix = self.ISSUE_COMMENT["prod"]
        version_str = PackageVersionNumber.parse_tag(
            self.release_notes_generator.current_tag, prefix_beta, prefix_prod
        ).format()
        has_comment = False
        for comment in self.jira.issue_get_comments(issue.key):
            if comment.body.startswith(comment_prefix):
                has_comment = True
                break
        if not has_comment:
            self.jira.issue_add_comment(issue.key, f"{comment_prefix} {version_str}")
