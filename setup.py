from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as req_file:
        return req_file.read().splitlines()


setup(
    name="CumulusCI-Jira",
    version="0.1",
    description="A plugin for CumulusCI that adds a service to connect to Atlassian's Jira including an integration with CumulusCI's release notes parser",
    author="Jason Lantz",
    author_email="jason@muselab.com",
    url="https://github.com/muselab-d2x/CumulusCI-Jira",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=read_requirements(),
    python_requires=">=3.10",
)
