# Generated by Django 5.0.7 on 2024-08-17 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='curr',
            field=models.CharField(default='MRU', max_length=100),
        ),
    ]
