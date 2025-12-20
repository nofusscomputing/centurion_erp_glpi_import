from django.db import models


class ZeroAsNoneForeignKey(models.ForeignKey):

    def __init__(self, to, related_name=None, related_query_name=None, limit_choices_to=None, parent_link=False, to_field=None, db_constraint=True, **kwargs):
        
        on_delete = models.DO_NOTHING

        if 'on_delete' in kwargs:
            del kwargs['on_delete']


        kwargs.update({
            'null': True,
        })

        super().__init__(to, on_delete, related_name, related_query_name, limit_choices_to, parent_link, to_field, db_constraint, **kwargs)

    def from_db_value(self, value, expression, connection):

        if value == 0:
            return None

        return value
