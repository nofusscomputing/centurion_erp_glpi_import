class GlpiImportRouter:

    db_alias = "glpi_import"


    def db_for_read(self, model, **hints):

        if not hasattr(model, '_meta'):
            return None

        if(
            model._meta.app_label == "glpi_import"
            and model._meta.model_name != 'glpiimportprogress'
        ):
            return self.db_alias

        return None


    def db_for_write(self, model, **hints):

        if(
            model._meta.app_label == "glpi_import"
            and model._meta.model_name != 'glpiimportprogress'
        ):
            return None

        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if db == self.db_alias:
            return False

        return None