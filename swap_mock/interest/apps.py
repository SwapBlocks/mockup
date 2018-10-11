from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InterestConfig(AppConfig):
    name = 'interest'
    verbose_name = _('interest')


    def ready(self):
        import interest.signals
