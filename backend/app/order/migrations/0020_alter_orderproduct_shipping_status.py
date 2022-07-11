# Generated by Django 3.2.7 on 2022-07-11 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_order_merchant_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='shipping_status',
            field=models.CharField(choices=[('미결제', '미결제'), ('결제완료', '결제완료'), ('상품준비중', '상품준비중'), ('배송중', '배송중'), ('배송완료', '배송완료')], default='미결제', max_length=8, verbose_name='배송상태'),
        ),
    ]
