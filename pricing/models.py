from django.db import models


class Detalles_tabla(models.Model):
    columna = models.CharField(max_length=128, blank=False, null=False)
    columna_excel = models.CharField(max_length=128, blank=False, null=False)
    detalles = models.CharField(max_length=256, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.columna + ' - ' + self.columna_excel + ' - ' + self.detalles


class Permissions(models.Model):
    generar_business_plan = 'pricing.generar_business_plan'

    class Meta:
        permissions = [
            ('generar_business_plan', 'Puede generar el business plan.'),
        ]
