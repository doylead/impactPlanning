# Generated by Django 3.2.4 on 2021-08-19 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gencal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
