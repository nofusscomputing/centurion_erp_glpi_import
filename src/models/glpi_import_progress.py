from enum import unique
from django.db import models

from access.fields import AutoCreatedField


class GlpiImportProgress(models.Model):

    class Meta:
        unique_together = [
            'glpi_id',
            'glpi_model_name',
            'glpi_hash',
        ]


    id = models.AutoField(
        blank=False,
        help_text = 'ID of the item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )


    glpi_id = models.IntegerField(
        blank = False,
        null = False,
        verbose_name = 'GLPI PK'
    )


    glpi_model_name = models.CharField(
        blank = False,
        max_length = 100,
        null = False,
        verbose_name = 'GLPI model_name'
    )


    glpi_hash = models.CharField( # sha256 of (model_kwargs)
        blank = False,
        max_length = 100,
        null = False,
        unique = True,
        verbose_name = 'GLPI model_name'
    )


    created = AutoCreatedField(
        editable = True
    )

