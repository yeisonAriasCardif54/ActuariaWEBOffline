from django.db import models

class Plantillas_presupuesto(models.Model):
    nombre = models.CharField(max_length=256, blank= False, null= False)
    descripcion = models.CharField(max_length=1024, blank=False, null = False)
    archivo = models.FileField(upload_to='plantillas/')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.nombre

class Permissions(models.Model):
    ver_reporte_pgv = 'profitability.ver_reporte_pgv'
    calcular_desembolsos_st_y_rrc = 'profitability.calcular_desembolsos_st_y_rrc'
    generar_presupuesto = 'profitability.generar_presupuesto'

    class Meta:
        permissions = [
            ('ver_reporte_pgv', 'Puede ver el reporte PGV.'),
            ('calcular_desembolsos_st_y_rrc', 'Puede calcular DesembolsosSt y RRC.'),
            ('generar_presupuesto', 'Puede generar el presupuesto.'),
            ('historico_presupuesto', 'Puede generar el historico de presupuestos generados.'),
            ('admin_grupo_presupuesto', 'Administrador del grupo de presupuestos generados.'),
        ]
