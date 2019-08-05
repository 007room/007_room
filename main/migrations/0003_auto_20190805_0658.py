# Generated by Django 2.1.7 on 2019-08-05 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190730_0846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qna',
            old_name='context',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='post_image',
            name='images',
            field=models.ImageField(blank=True, upload_to='image/post_image/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='qna_image',
            name='images',
            field=models.ImageField(blank=True, upload_to='image/qna_image/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='review_image',
            name='images',
            field=models.ImageField(blank=True, upload_to='image/review_image/%Y/%m/%d'),
        ),
    ]
