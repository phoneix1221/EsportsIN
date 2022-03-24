from django.apps import AppConfig


class ModmainConfig(AppConfig):
    name = 'modmain'

    def ready(self):
        import modmain.signals
