from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class ShippingStatusChoices(models.TextChoices):
    UNPAID = '미결제', '미결제'
    PAID = '결제완료', '결제완료'
    READY = '상품준비중', '상품준비중'
    SHIPPING = '배송중', '배송중'
    SHIPPED = '배송완료', '배송완료'
    CANCELLED = '주문취소', '주문취소'


class PayMethodChoices(models.TextChoices):
    CARD = '신용카드', '신용카드'


class Order(models.Model):
    user = models.ForeignKey('user.User', verbose_name="주문자", related_name="orders", on_delete=models.CASCADE)
    merchant_uid = models.CharField(verbose_name="주문번호", max_length=16, unique=True, default="ORD000000-000000")
    imp_uid = models.CharField(verbose_name="결제번호", max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="주문일시", auto_now_add=True)
    shipping_name = models.CharField(verbose_name="수령인", max_length=10)
    shipping_phone = models.CharField(verbose_name="전화번호", max_length=13)
    shipping_zipcode = models.CharField(verbose_name="우편번호", max_length=7)
    shipping_address = models.CharField(verbose_name="배송주소", max_length=1000)
    shipping_address_detail = models.CharField(verbose_name="배송상세주소", max_length=1000, null=True, blank=True)
    shipping_request = models.CharField(verbose_name="배송요청사항", max_length=300, null=True, blank=True)
    shipping_status = models.CharField(verbose_name="배송상태", choices=ShippingStatusChoices.choices, max_length=8,
                                       default="미결제")
    pay_method = models.CharField(verbose_name="결제수단", choices=PayMethodChoices.choices, max_length=4, default="신용카드")
    pay_date = models.DateField(verbose_name="결제일자", auto_now_add=True)
    total_price = models.IntegerField(verbose_name="총 상품금액", validators=[MinValueValidator(0)])
    delivery_fee = models.IntegerField(verbose_name="배송비")
    total_paid = models.IntegerField(verbose_name="결제금액", validators=[MinValueValidator(0)], default=0)
    cancel_amount = models.IntegerField(verbose_name="환불금액", validators=[MinValueValidator(0)], default=0)

    class Meta:
        verbose_name = "주문"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Order {self.merchant_uid} - {self.user}'


class OrderProduct(models.Model):
    order = models.ForeignKey('order.Order', verbose_name="주문", related_name="order_products", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', verbose_name="상품", related_name="order_products",
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="수량", validators=[MinValueValidator(1)])
    price = models.IntegerField(verbose_name="상품가격", validators=[MinValueValidator(0)])
    shipping_status = models.CharField(verbose_name="배송상태", choices=ShippingStatusChoices.choices, max_length=8,
                                       default="미결제")

    class Meta:
        verbose_name = "주문-상품"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]

    def __str__(self):
        return f'OrderProduct({self.id}) - Order {self.order.merchant_uid} - {self.product}'
