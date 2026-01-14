from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from core.mixins.centurion import Centurion

SkipMigration: Exception = import_string(
    dotted_path = f"{apps.app_configs['glpi_import'].name}.exceptions.SkipMigration"
)



def empty_str_to_none(value: str) -> str | None:

    if value == '':
        return None

    return value



def value_substitution(value, glpi_model_name) -> str:

    substitutions = settings.GLPI_IMPORT['substitutions']

    if glpi_model_name not in substitutions:
        return value

    if value not in substitutions[glpi_model_name]:
        return value

    return substitutions[glpi_model_name][value]



def glpi_to_centurion(
    field: models.Field,
    field_value,
    # model: models.Model:
    object_dict: dict,
    create = False
):

    app_label, model_name = object_dict['centurion_model'].split('.')

    centurion_model = apps.get_model(
        app_label = app_label,
        model_name = model_name
    )

    existing = []

    centurion_model_filter_kwargs = {
        f"{object_dict.get('match_field_name', 'name')}__iexact": ''
    }

    if field_value is None:

        if field.name == 'entities':

            centurion_model_filter_kwargs.update({
                f"{object_dict.get('match_field_name', 'name')}__iexact": 'Common'
            })

            existing = centurion_model.objects.filter(
                # name__iexact = 'Common'
                **centurion_model_filter_kwargs
            )

        else:

            return None


    else:

        value = value_substitution( value = field_value.name, glpi_model_name = field.name)

        existing = centurion_model.objects.filter(
            name__iexact = value
        )


    if len(existing) == 0:

        # To Do: Check field length

        if not object_dict.get('create', False):
            return None

        progress_model = apps.get_model(
            app_label = 'glpi_import',
            model_name = 'glpiimportprogress'
        )

        if field_value._meta.model_name in settings.GLPI_IMPORT['objects']:

            model_kwargs = get_model_kwargs(
                object_dict = settings.GLPI_IMPORT['objects'][field_value._meta.model_name],
                glpi_data = field_value
            )

            app_label, model_name = object_dict['centurion_model'].split('.')

            centurion_model = apps.get_model(
                app_label = app_label,
                model_name = model_name
            )


            system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
                username = 'system'
            ).first()


            existing = centurion_model(
                **model_kwargs
            )

            type(existing).context.update({
                existing._meta.model_name: system_user
            })

            existing.full_clean()

            if create:

                existing.save()

                from .tasks.import_model import entry_hash

                hash = entry_hash(model_kwargs = model_kwargs)

                progress_model.objects.create(
                    glpi_id = field_value.id,
                    glpi_model_name = field_value._meta.model_name,
                    glpi_hash = hash,
                )

                print( f'created: {field_value._meta.model_name}={model_kwargs}' )

                del type(existing).context[existing._meta.model_name]

            else:

                existing = None


    elif len(existing) == 1:

        print( f'found: {model_name}' )

        existing = existing.first()

    elif len(existing) > 1:

        raise LookupError( f'{len(existing)} objects were returned for manufacturer with name {field_value.name} and value {value}.' )

    else:
        existing = existing.first()


    return existing



def get_model_kwargs(
    object_dict: dict,
    glpi_data,
    create = False
) -> dict:

    kwargs: dict = {}

    app_label, model_name = object_dict['glpi_model'].split('.')

    glpi_model = apps.get_model(
        app_label = app_label,
        model_name = model_name
    )

    app_label, model_name = object_dict['centurion_model'].split('.')

    centurion_model = apps.get_model(
        app_label = app_label,
        model_name = model_name
    )

    glpi_field_names = [ field.name for field in glpi_model._meta.get_fields() ]

    centurion_field_names = [ field.name for field in centurion_model._meta.get_fields() ]

    for centurion_field_name, glpi_field_name in object_dict['centurion_glpi_field_map'].items():

        if centurion_field_name not in centurion_field_names:
            continue    # Raise Error non-existant centurion field

        if glpi_field_name not in glpi_field_names:
            continue    # Raise Error non-existant glpi field


        field = getattr(glpi_data, glpi_field_name)

        if(
            isinstance(field, models.Model)
            or field is None
        ):

            field_model_name = glpi_data._meta.get_field(glpi_field_name).related_model._meta.model_name

            if field_model_name in settings.GLPI_IMPORT['objects']:

                field = glpi_to_centurion(
                    field = glpi_data._meta.get_field(glpi_field_name),
                    field_value = field,
                    object_dict = settings.GLPI_IMPORT['objects'][field_model_name],
                    create = create,
                )

                if isinstance(field, models.Model):
                    if not isinstance(field, Centurion):
                        print( f'{field_model_name} is not a Centurion Model-1' )

            else:

                print( f'{field_model_name} has no map defined.' )
                raise SkipMigration(f'{field_model_name} has no map defined.')


        elif isinstance(field, str):

            field = empty_str_to_none(value = field)


        if isinstance(field, models.Model):
            if not isinstance(field, Centurion):
                    print( f'{field_model_name} is not a Centurion Model-2' )


        kwargs.update({
            centurion_field_name: field
        })


    if len(object_dict['centurion_glpi_field_map']) != len(kwargs):
        return None    # Error not all fields were added


    return kwargs
