# Generated by Django 2.1.7 on 2019-08-08 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='application',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
