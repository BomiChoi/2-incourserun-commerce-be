# Generated by Django 3.2.7 on 2022-06-27 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20220627_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='img',
            field=models.ImageField(upload_to='review', verbose_name='이미지'),
        ),
    ]
