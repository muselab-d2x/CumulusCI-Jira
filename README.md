# CumulusCI JIRA Plugin


[![PyPI version](https://badge.fury.io/py/CumulusCI-Jira.svg)](https://badge.fury.io/py/CumulusCI-Jira)
![versions](https://img.shields.io/pypi/pyversions/CumulusCI-Jira.svg)
[![GitHub license](https://img.shields.io/github/license/mgancita/CumulusCI-Jira.svg)](https://github.com/mgancita/CumulusCI-Jira/blob/main/LICENSE)


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


A plugin for CumulusCI that adds a service to connect to Atlassian's Jira including an integration with CumulusCI's release notes parser
# WARNING: This installs a non-production release of CumulusCI and experimental plugin code
```
pip install git+https://github.com/muselab-d2x/CumulusCI-Jira
```

Add the following to your cumulusci.yml file to enable the plugin:
```
plugins:
    - cumulusci_jira
```

## Reset your CumulusCI:
```
pip uninstall cumulusci_jira
pip uninstall cumulusci
pip install cumulusci
```

- Free software: BSD-3-Clause
- Documentation: https://jlantz.github.io/CumulusCI-Jira.


## Features

* TODO

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`mgancita/cookiecutter-pypackage`](https://mgancita.github.io/cookiecutter-pypackage/) project template.
