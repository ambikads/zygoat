import logging

from zygoat.components import Component
from zygoat.constants import Phases
from zygoat.utils.backend import install_dependency

log = logging.getLogger()


class Dependencies(Component):
    def create(self):
        dependencies = [
            "Django",
            "psycopg2-binary",
            "django-cors-headers",
            "djangorestframework",
            "django-environ",
        ]

        dev_dependencies = ["django-anymail", "pytz", "factory-boy"]

        for dep in dependencies:
            log.info(f"Installing {dep}")
            install_dependency(dep)

        for dep in dev_dependencies:
            log.info(f"Installing {dep}")
            install_dependency(dep, dev=True)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


dependencies = Dependencies()
