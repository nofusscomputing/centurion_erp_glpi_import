import os

from django.apps import AppConfig



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
