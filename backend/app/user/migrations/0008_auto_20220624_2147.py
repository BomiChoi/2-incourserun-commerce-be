# Generated by Django 3.2.7 on 2022-06-24 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_cart_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='profile', verbose_name='프로필사진'),
        ),
    ]
