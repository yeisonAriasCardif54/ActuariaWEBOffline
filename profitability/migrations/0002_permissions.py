# Generated by Django 2.1.3 on 2019-01-14 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profitability', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('ver_reporte_pgv', 'Puede ver el reporte PGV.'), ('calcular_desembolsos_st_y_rrc', 'Puede calcular DesembolsosSt y RRC.'), ('generar_presupuesto', 'Puede generar el presupuesto')],
            },
        ),
    ]
