# Generated by Django 2.1.3 on 2019-01-21 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profitability', '0002_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permissions',
            options={'permissions': [('ver_reporte_pgv', 'Puede ver el reporte PGV.'), ('calcular_desembolsos_st_y_rrc', 'Puede calcular DesembolsosSt y RRC.'), ('generar_presupuesto', 'Puede generar el presupuesto.'), ('historico_presupuesto', 'Puede generar el historico de presupuestos generados.'), ('admin_grupo_presupuesto', 'Administrador del grupo de presupuestos generados.')]},
        ),
    ]
