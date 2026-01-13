import os

from django.apps import AppConfig
from django.conf import settings



class GlpiImportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "glpi_import"
    label = 'glpi_import'


    def __init__(self, app_name, app_module):
        """ Wrapper

        This wrapper exists to enable the repository directory structure
        to be included as a Django app during development. all that is required
        is the following:
            - repository be cloned to `<centurion erp>/glpi_import/`
            - following file exists `<centurion erp>/glpi_import/__init__.py`
            - Settings.installed apps updated from 'glpi_import.src.apps.GlpiImportConfig`
              to 'glpi_import.src.apps.GlpiImportConfig`
        """

        parent_dir = os.path.basename(os.path.dirname(__file__))

        if parent_dir != self.label:
            self.name = f'{self.label}.{parent_dir}'
            app_name = self.name
            app_module = getattr(app_module, parent_dir)


        super().__init__(app_name, app_module)



    def ready(self):

        if not settings.RUNNING_TESTS:

            if(
                os.environ.get(f"{str(self.label).upper()}_DB_USER", None)
                and os.environ.get(f"{str(self.label).upper()}_DB_PASSWORD", None)
            ):

                settings.DATABASES.update({
                    self.label: {
                        "ENGINE": "django.db.backends.mysql",
                        "NAME": os.environ.get(f"{str(self.label).upper()}_DB_NAME", 'glpi'),
                        "USER": os.environ.get(f"{str(self.label).upper()}_DB_USER", ''),
                        "PASSWORD": os.environ.get(f"{str(self.label).upper()}_DB_PASSWORD", ''),
                        "HOST": os.environ.get(f"{str(self.label).upper()}_DB_HOST", '127.0.0.1'),
                        "PORT": os.environ.get(f"{str(self.label).upper()}_DB_PORT", "3306"),
                        "ATOMIC_REQUESTS": False,
                        "TIME_ZONE": None,
                        "CONN_MAX_AGE": 0,
                        "OPTIONS": {
                            "init_command": "SET SESSION TRANSACTION READ ONLY",
                        },
                    },
                })


            settings.DATABASE_ROUTERS = [
                f"{self.name}.db_router.GlpiImportRouter",
                *settings.DATABASE_ROUTERS,
            ]
