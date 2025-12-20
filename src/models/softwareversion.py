from django.db import models

from .entities import GlpiEntities
from .fields.zero_foriegnkey import ZeroAsNoneForeignKey
from .software import GlpiSoftwares



class GlpiSoftwareversions(models.Model):
    entities = ZeroAsNoneForeignKey( to = GlpiEntities, db_column = 'entities_id' )
    is_recursive = models.IntegerField()
    softwares = ZeroAsNoneForeignKey( to = GlpiSoftwares, db_column = 'softwares_id', related_name = 'versions' )
    states_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    arch = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    operatingsystems_id = models.PositiveIntegerField()
    date_mod = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glpi_softwareversions'
