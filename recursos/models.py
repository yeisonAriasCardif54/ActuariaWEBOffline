from django.db import models


# Create your models here.

class Permissions(models.Model):
    recursos_matriz_implementacion = 'recursos.recursos_matriz_implementacion'
    informe_superintendencia = 'recursos.informe_superintendencia'

    class Meta:
        permissions = [
            ('recursos_matriz_implementacion', 'Puede descargar las matrices de configuración para implementación.'),
            ('informe_superintendencia', 'Puede ver los reportes de la superintendencia financiera'),
        ]
