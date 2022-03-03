# Generated by Django 3.1.2 on 2022-03-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_camara', models.CharField(max_length=200)),
                ('fecha_publicacion_camara', models.DateTimeField(verbose_name='date published')),
                ('descripcion_camara', models.CharField(max_length=500)),
            ],
        ),
    ]
