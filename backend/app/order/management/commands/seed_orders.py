import random
from datetime import date, datetime

from app.order.models import Order, OrderProduct
from app.product.models import Product
from app.user.models import User
from django.contrib.admin.utils import flatten
from django.core.management.base import BaseCommand
from django.db import transaction
from django_seed import Seed
from faker import Faker


class Command(BaseCommand):
    help = "This command creates orders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many orders you want to create"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        n = options.get("number")
        all_users = User.objects.all()

        for _ in range(n):
            seeder = Seed.seeder()
            faker = Faker('ko_KR')
            status = random.choice(['결제완료', '상품준비중', '배송중', '배송완료'])
            seeder.add_entity(
                Order,
                1,
                {
                    "user": random.choice(all_users),
                    "shipping_name": faker.name(),
                    "shipping_phone": faker.phone_number(),
                    "shipping_zipcode": seeder.faker.zipcode(),
                    "shipping_address": faker.address(),
                    "shipping_address_detail": "",
                    "shipping_request": "",
                    "shipping_status": status,
                    "pay_method": "신용카드",
                    "pay_date": date.today(),
                    "total_price": 0,
                    "delivery_fee": 0,
                    "created_at": datetime.now()
                }
            )

            created_orders = seeder.execute()
            created_clean = flatten(list(created_orders.values()))
            total_price = 0
            for pk in created_clean:
                order = Order.objects.get(pk=pk)
                order.merchant_uid = f'ORD{order.created_at.strftime("%y%m%d")}-{str(order.id).zfill(6)}'
                products = random.sample(list(Product.objects.all()), random.randint(1, 5))
                for product in products:
                    quantity = random.randint(1, 5)
                    OrderProduct.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                        shipping_status=status
                    )
                    total_price += product.price * quantity
                order.total_price = total_price
                if total_price < 30000:
                    order.delivery_fee = 3000
                order.total_paid = order.total_price + order.delivery_fee
                order.save()

        self.stdout.write(self.style.SUCCESS(f"{n} orders created"))
