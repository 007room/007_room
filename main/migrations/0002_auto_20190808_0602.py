# Generated by Django 2.1.7 on 2019-08-08 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='context',
            new_name='text',
        ),
    ]