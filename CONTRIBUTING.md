# Contribution Guide

Contributions to this project are welcome. Development of this project has been setup to be done from VSCodium.


## Setup dev environment

1. Clone the repository to the Django app directory ( i.e for Centurion ERP `app/glpi_import`)

2. within the repo root add empty file `__init__.py`

3. Add to your django settings `INSTALLED_APPS` value `'glpi_import.src.apps.GlpiImportConfig'`

    _Note: the `.src.` in the path. This is only required when the repo is cloned._

4. Start the django app as normal.
