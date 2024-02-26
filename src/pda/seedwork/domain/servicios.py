""" Definición de interfaces de Servicios reusables parte del seedwork del proyecto

En este archivo usted encontrará las diferentes interfaces para Servicios
reusables parte del seedwork del proyecto

"""

from .mixins import ValidateMixinRules


class Servicio(ValidateMixinRules): ...
