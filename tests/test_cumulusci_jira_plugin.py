"""Test module for cumulusci_jira_plugin."""

from cumulusci_jira import __author__, __email__, __version__


def test_project_info():
    """Test __author__ value."""
    assert __author__ == "Jason Lantz"
    assert __email__ == "jason@muselab.com"
    assert __version__ == "0.1"
