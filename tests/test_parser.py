import unittest
import vcr
from cumulusci_jira.parser import JiraIssuesParser

my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="fixtures/vcr_cassettes",
    record_mode="once",
    match_on=["uri", "method"],
)


class TestJiraIssuesParser(unittest.TestCase):
    def setUp(self):
        # Set up your mock release_notes_generator with necessary attributes
        self.release_notes_generator = Mock()
        self.release_notes_generator.project_config = Mock()
        self.release_notes_generator.project_config.keychain = Mock()
        self.release_notes_generator.link_pr = True
        self.release_notes_generator.do_publish = True

        # Initialize the JiraIssuesParser instance
        self.parser = JiraIssuesParser(self.release_notes_generator, "Jira Issues Closed")

        # Mock data for testing
        self.parser.content = [
            {
                "issue_number": 123,
                "issue_key": "TEST-123",
                "pr_number": 456,
                "pr_url": "http://example.com/pr/456",
            }
            # Add more mock issue data as needed
        ]

    @my_vcr.use_cassette("test_render_content.yml")
    def test_render_content(self):
        # Test the _render_content method
        content = self.parser._render_content()

        # Assertions to check if the content is rendered correctly
        self.assertIn("#TEST-123: ", content)
        self.assertIn(" [PR456](http://example.com/pr/456)", content)
        # Add more assertions based on your expected output

        # Verify interactions with Jira API, if applicable


if __name__ == "__main__":
    unittest.main()
