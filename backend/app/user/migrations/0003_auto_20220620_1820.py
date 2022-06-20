# Generated by Django 3.2.7 on 2022-06-20 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220620_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='주소'),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(blank=True, choices=[('teen', '10대'), ('twenty', '20대'), ('thirty', '30대'), ('forty', '40대'), ('fifty', '50대 이상')], max_length=6, null=True, verbose_name='연령대'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', '남성'), ('female', '여성')], max_length=6, null=True, verbose_name='성별'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='', max_length=10, verbose_name='닉네임'),
            preserve_default=False,
        ),
    ]
