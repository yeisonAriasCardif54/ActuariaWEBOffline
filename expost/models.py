from django.db import models

# Create your models here.
class Permissions(models.Model):
    generar_business_plan = 'expost.ver_reportes'

    class Meta:
        permissions = [
            ('ver_reportes', 'Puede ver todos los reportes'),
        ]
