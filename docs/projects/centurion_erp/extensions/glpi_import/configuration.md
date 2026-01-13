---
title: Configuration
description: Documentation home on how to configure Centurion ERP Extension GLPI Import by No Fuss Computing
date: 2026-01-13
template: project.html
about: https://github.com/nofusscomputing/centurion_erp_glpi_import
---

An extension to import data from GLPI.


## Configuration

To configure what to import create a dict within Centurion ERP settings called `GLPI_IMPORT`. This dictionary will contain the configuration to migrate the data from GLPI to Centurion ERP.

``` py

GLPI_IMPORT = {
    "objects": {},
    "substitutions": {}
}

```


## Objects

To import objects from the GLPI to Centurion ERP, add the configuration to the `objects` key. The structure of `objects` is as follows:

``` py
"objects": {
    "<GLPI Model Name>": {
        "glpi_model": "glpi_import.glpientities",    # GLPI model in format <app_label>.<model_name>
        "centurion_model": "access.tenant",          # Centurion model in format <app_label>.<model_name>
        "centurion_glpi_field_map": {                # Centurion to GLPI model fields map
            "name": "name",                          # format is <Centurion Model field name>: <GLPI Model field name>
            "model_notes": "comment",
            "created": "date_creation",
        },
        "match_field_name": "name",                  # the field that is used to locate a duplicate/existing.
        "create": False,                             # Create the Centurion Model if it doesn't exist
    }
}
```


## Value Mapping

There may be occasion where you need to map a field value to another value. This can be done by adding the `substitutions` key to the config dict. The structure of `substitutions` is as follows:


``` py

"substitutions": {
    "<Centurion Model Name>": {
        "<Original Value>": "<New value>",
    }
}

```


## Database setup

This extension requires direct access to the GLPI database. To do enable this configure the following environmental variables:

- `GLPI_IMPORT_DB_NAME` _Optional, default=`glpi`_ - Name of the GLPI database to configure.

- `GLPI_IMPORT_DB_USER` _Required_ - Name of the database user to connect to the GLPI database.

- `GLPI_IMPORT_DB_PASSWORD` _Required_ - Password for the database user to connect to GLPI database.

- `GLPI_IMPORT_DB_HOST` _Optional, default=`127.0.0.1`_ - Host of the database server.

- `GLPI_IMPORT_DB_PORT` _Optional, default=`3306`_ port for the database server.
