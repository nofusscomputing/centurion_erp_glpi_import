---
title: Add Glpi Table
description: Documentation home on how to add a GLPI Table to Centurion ERP Extension GLPI Import by No Fuss Computing
date: 2026-01-13
template: project.html
about: https://github.com/nofusscomputing/centurion_erp_glpi_import
---

Adding a table that can be used for import is as simple as running command `./manage.py inspectdb -v2 --database glpi_import > /app/glpi_import/src/all_models.py` and updating the auto-generated table fields.


## id / pk fields

any field that contains `_id` are generally related to a table. this should be linked to a model.

i.e.

``` py
from django.db import models

from .entities import GlpiEntities
from .fields.zero_foriegnkey import ZeroAsNoneForeignKey



class GlpiChanges(models.Model):

    entities_id = models.PositiveIntegerField(blank=True, null=True)

    # would be updated to
    entities = ZeroAsNoneForeignKey(      # truncate the `_id` as it's not required.
        to = GlpiEntities,
        on_delete = models.DO_NOTHING,    # set this attr as it is here. django should not be modifying data
        db_column = 'entities_id',        # This must be the name of the db column. normally this is the original python variable name
        related_name = 'changes'          # this is the name the field will use on the linked model. in this case `GlpiEntities`
    )

```

!!! tip
    GLPI id/PK fields can have a value of `0`. This causes issues as this is a primary key which must contain a value that is either `null` or an integer above `0`. To correct this action set all id/pk fields to use custom field `models.fields.zero_foriegnkey.ZeroAsNoneForeignKey`
