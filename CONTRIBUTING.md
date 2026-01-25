# Contribution Guide

Contributions to this project are welcome. Development of this project has been setup to be done from VSCodium.


## Setup dev environment

1. Clone the repository.

1. Add to your django settings `INSTALLED_APPS` value `'glpi_import.apps.GlpiImportConfig'`.

1. create your virtual env and activate.

1. Install current app in edit mode `pip install -e .`.

1. Create module `ln -s ${PWD}$/src ---venv path---/lib/python3.11/site-packages/glpi_import`.

    _This is required as the package is a namespace package and without it, ide imports dont work._

1. Start the django app as normal.
