from django.db import models

from .entities import GlpiEntities
from .fields.zero_foriegnkey import ZeroAsNoneForeignKey
from .manufacturer import GlpiManufacturers
from .softwarecategory import GlpiSoftwarecategories
from .users import GlpiUsers



class GlpiSoftwares(models.Model):
    entities = ZeroAsNoneForeignKey( to = GlpiEntities, db_column = 'entities_id' )
    is_recursive = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    locations_id = models.PositiveIntegerField()
    users_id_tech = models.PositiveIntegerField()
    is_update = models.IntegerField()
    softwares_id = models.PositiveIntegerField()
    manufacturer = ZeroAsNoneForeignKey( to = GlpiManufacturers, db_column = 'manufacturers_id', related_name = 'software')
    is_deleted = models.IntegerField()
    is_template = models.IntegerField()
    template_name = models.CharField(max_length=255, blank=True, null=True)
    date_mod = models.DateTimeField(blank=True, null=True)
    users = ZeroAsNoneForeignKey( to = GlpiUsers, db_column = 'users_id', related_name = '+' )
    ticket_tco = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    is_helpdesk_visible = models.IntegerField()
    softwarecategories = ZeroAsNoneForeignKey( to = GlpiSoftwarecategories, db_column = 'softwarecategories_id', related_name = 'software')
    is_valid = models.IntegerField()
    date_creation = models.DateTimeField(blank=True, null=True)
    pictures = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glpi_softwares'
