# Generated by Django 2.1.3 on 2019-08-28 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('recursos_matriz_implementacion', 'Puede descargar las matrices de configuración para implementación.'), ('informe_superintendencia', 'Puede ver los reportes de la superintendencia financiera')],
            },
        ),
    ]
