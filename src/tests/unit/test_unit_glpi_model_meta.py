import pytest

from django.apps import apps
from django.db import models
from django.utils.module_loading import import_string


class GlpiModelTestCases:

    @pytest.fixture( scope = 'class' )
    def foreignkey_class(self):

        yield import_string(f"{apps.app_configs['glpi_import'].name}.models.fields.zero_foriegnkey.ZeroAsNoneForeignKey")



    def test_class_meta_attribute_managed(self):
        """Test Meta class attribute
        
        ALL GLPI models must have `managed=False` attribute within the meta
        class.
        """

        assert 'managed' in self.model_class._meta.original_attrs, 'Test cant continue without the required attribute'

        assert self.model_class._meta.managed == False



    def test_class_meta_attribute_db_table(self):
        """Test Meta class attribute
        
        ALL GLPI models must have `db_table=<actual db name>` attribute within the meta
        class.
        """

        assert 'db_table' in self.model_class._meta.original_attrs, 'Test cant continue without the required attribute'




    @property
    def parameterized_foreignkey_fields(self): 
        vals = {}

        for field in [
            meta_field for meta_field in self.model_class._meta.fields if issubclass(type(meta_field), models.ForeignKey)
        ]:

            vals.update({
                field.name: {
                    'field': field
                }
            })

        return vals


    def test_class_meta_attribute_foreignkey_field(self, 
        foreignkey_class,
        parameterized, param_key_foreignkey_fields,
        param_value,
        param_field
    ):
        """Test Meta class attribute
        
        ALL GLPI models must have `db_table=<actual db name>` attribute within the meta
        class.
        """

        assert issubclass(type(param_field), foreignkey_class), 'Wrong Field type.'







def get_models( excludes: list[ str ] = [] ) -> list[ tuple ]:
    """Fetch models from Centurion Apps

    Args:
        excludes (list[ str ]): Words that may be in a models name to exclude

    Returns:
        list[ tuple ]: Centurion ERP Only models
    """

    models: list = []

    model_apps: list = [
        'glpi_import'
    ]

    exclude_model_apps = []


    for model in apps.get_models():

        model_name = str(model._meta.model_name)

        if(
            model._meta.app_label not in model_apps
            or not str(model_name).startswith('glpi')
        ):
            continue

        skip = False

        for exclude in excludes:

            if exclude in str(model._meta.model_name):
                skip = True
                break

        if skip:
                continue

        models += [ model ]

    return models




for model in get_models():

    if not str(model._meta.object_name).startswith('Glpi'):
        continue


    cls_name: str = f"{model._meta.object_name}MetaGlpiModelPyTest"

    dynamic_class = type(
        cls_name,
        (GlpiModelTestCases,),
        {
            'model_class': model
        }
    )

    globals()[cls_name] = dynamic_class
