# Generated by Django 3.2.7 on 2022-07-08 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_merge_20220708_1541'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_number',
            new_name='marchant_uid',
        ),
    ]
