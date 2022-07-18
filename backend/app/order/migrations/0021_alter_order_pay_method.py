# Generated by Django 3.2.7 on 2022-07-18 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_alter_orderproduct_shipping_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_method',
            field=models.CharField(choices=[('신용카드', '신용카드')], default='신용카드', max_length=4, verbose_name='결제수단'),
        ),
    ]
