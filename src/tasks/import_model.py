import hashlib

from celery import shared_task
from celery.utils.log import get_task_logger

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError

from centurion_erp.centurion.logging import CenturionLogger

from glpi_import.process import (
    empty_str_to_none,
    get_model_kwargs,
    SkipMigration,
    value_substitution,
)



def entry_hash(model_kwargs: dict) -> str:

    hash_vals = model_kwargs.copy()

    if 'created' in hash_vals:
        del hash_vals['created']

    vals = []
    for key, value in hash_vals.items():
        if type(value) not in [ str, int]:
            vals += [ str(value) ]
            continue

        vals += [ value ]


    combined = "|".join(vals)
    return hashlib.sha256(string = combined.encode("utf-8")).hexdigest()



@shared_task( bind = True )
def glpi_import(self, object_dict: dict):

    logger: CenturionLogger = get_task_logger( name = __name__ )

    logger.info( msg = 'Begin Import' )

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

    progress_model = apps.get_model(
        app_label = 'glpi_import',
        model_name = 'glpiimportprogress'
    )

    system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
        username = 'system'
    ).first()


    for glpi_data in glpi_model.objects.all():

        try:

            centurion_model_kwargs = get_model_kwargs(
                    object_dict = object_dict,
                    glpi_data = glpi_data,
                    create = True,
                )

            hash = entry_hash(model_kwargs = centurion_model_kwargs)

            progress_entry = progress_model.objects.filter(
                glpi_model_name = glpi_data._meta.model_name,
                glpi_hash = hash,
            )


            if len(progress_entry) == 0:

                logger.info( msg = f'Processing model {glpi_data._meta.model_name} id={glpi_data.id}' )

                centurion = centurion_model(
                    **centurion_model_kwargs
                )

                centurion.full_clean()


                type(centurion).context.update({
                    centurion._meta.model_name: system_user
                })

                centurion.save()

                progress_model.objects.create(
                    glpi_id = glpi_data.id,
                    glpi_model_name = glpi_data._meta.model_name,
                    glpi_hash = hash,
                )

                del type(centurion).context[centurion._meta.model_name]

                logger.info( msg = f'Migrated model {glpi_data._meta.model_name} id={glpi_data.id}' )


            #
            # Process sub-models
            #
            for field_name, glpi_model in object_dict['sub_models'].items():

                for sub_glpi_data in getattr(glpi_data, field_name).all():    # Fetch All sub-models

                    sub_object_dict = settings.GLPI_IMPORT['objects'][glpi_model]

                    sub_app_label, sub_model_name = sub_object_dict['glpi_model'].split('.')

                    sub_glpi_model = apps.get_model(
                        app_label = sub_app_label,
                        model_name = sub_model_name
                    )

                    sub_app_label, sub_model_name = sub_object_dict['centurion_model'].split('.')

                    sub_centurion_model = apps.get_model(
                        app_label = sub_app_label,
                        model_name = sub_model_name
                    )


                    sub_centurion_model_kwargs = get_model_kwargs(
                            object_dict = sub_object_dict,
                            glpi_data = sub_glpi_data,
                            create = True,
                        )


                    sub_hash = entry_hash(model_kwargs = sub_centurion_model_kwargs)

                    sub_progress_entry = progress_model.objects.filter(
                        glpi_model_name = sub_glpi_model._meta.model_name,
                        glpi_hash = sub_hash,
                    )


                    if len(sub_progress_entry) == 0:

                        logger.info( msg = f'Processing sub-model {sub_glpi_data._meta.model_name} id={sub_glpi_data.id}' )

                        centurion = sub_centurion_model(
                            **sub_centurion_model_kwargs
                        )

                        centurion.full_clean()

                        type(centurion).context.update({
                            centurion._meta.model_name: system_user
                        })

                        centurion.save()

                        progress_model.objects.create(
                            glpi_id = sub_glpi_data.id,
                            glpi_model_name = sub_glpi_model._meta.model_name,
                            glpi_hash = sub_hash,
                        )

                        del type(centurion).context[centurion._meta.model_name]

                        logger.info( msg = f'Migrated sub-model {sub_glpi_data._meta.model_name} id={sub_glpi_data.id}' )


        except ValidationError as e:
            logger.notice( msg = f'Validation error occured: {e}' )

        except SkipMigration as e:
            logger.warning( msg = f'Object not migrated: {e}' )

        except Exception as e:
            logger.critical( msg = f'Unknown error occured: {e}' )


    logger.info( msg = 'End Import' )

