from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Order, OrderProduct
from ..review.serializers import ReviewSerializer
from django.contrib.auth import get_user_model


class OrderProductSerializer(serializers.ModelSerializer):
    has_review = serializers.BooleanField(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'quantity', 'price', 'shipping_status', 'is_cancelled', 'has_review')


class OrderProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('is_cancelled',)

    def update(self, instance, validated_data):
        if instance.shipping_status != "결제완료":
            raise ValidationError({'status':'상품이 결제완료 상태일 때만 변경 가능합니다.'})
        instance.is_cancelled = validated_data['is_cancelled']

        # 총 주문금액 업데이트
        order = instance.order
        if instance.is_cancelled:
            # 주문취소
            order.total_price -= instance.price * instance.quantity
            if order.total_price == 0:
                order.is_cancelled = True
                order.delivery_fee = 0
            elif order.total_price < 30000:
                order.delivery_fee = 3000
        else:
            # 주문취소 철회
            order.is_cancelled = False
            order.total_price += instance.price * instance.quantity
            if order.total_price < 30000:
                order.delivery_fee = 3000
            else:
                order.delivery_fee = 0
        instance.save()
        order.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    User = get_user_model()
    order_products = OrderProductSerializer(many=True)
    order_number = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'created_at',
            'imp_uid',
            'order_number',
            'shipping_name',
            'shipping_phone',
            'shipping_zipcode',
            'shipping_address',
            'shipping_address_detail',
            'shipping_request',
            'shipping_status',
            'pay_method',
            'pay_date',
            'total_price',
            'delivery_fee',
            'total_paid',
            'cancel_amount',
            'is_cancelled',
            'order_products'
        )

    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
        order_products = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        order.order_number = order.created_at.strftime("%y%m%d") + str(order.id).zfill(4)
        order.save()
        for order_product in order_products:
            OrderProduct.objects.create(order=order, **order_product)
        return order

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('is_cancelled',)

    def update(self, instance, validated_data):
        print(instance)
        if instance.shipping_status != "결제완료":
            raise ValidationError({'status':'주문이 결제완료 상태일 때만 변경 가능합니다.'})
        instance.is_cancelled = validated_data['is_cancelled']
        return instance
        

class CancelSerializer(serializers.Serializer):
    merchant_uid = serializers.CharField(write_only=True)
    cancel_request_amount = serializers.CharField(write_only=True)
    reason = serializers.CharField(write_only=True)
    result = OrderSerializer(read_only=True)

    def validate(self, attrs):
        merchant_uid = attrs['merchant_uid']
        # 결제정보 조회
        order = get_object_or_404(Order, order_number=merchant_uid)
        imp_uid, amount, cancel_amount  = order.imp_uid, order.total_paid, order.cancel_amount
        cancelable_amount = amount - cancel_amount
        if cancelable_amount <= 0:
            raise ValidationError({"merchant_uid":"이미 전액환불된 주문입니다."})
        
        # 결제환불 요청
        url = "https://api.iamport.kr/payments/cancel"
        data = {
            'imp_uid': imp_uid,
            'amount': attrs['cancel_request_amount'],
            'reason': attrs['reason'],
            'checksum': cancelable_amount,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('IAMPORT CANCEL API ERROR')
            print(response.content)

        data = response.json()
        # 응답 코드가 200이라도 응답 body의 code가 0이 아니면 환불에 실패했다는 의미
        if data['code'] != 0: 
            msg = data['message']
            raise ValidationError(f'환불 실패: {msg}')
        return data

    def create(self, validated_data):
        response = validated_data['response'] # 환불 결과

        # 환불 결과 동기화
        merchant_uid = data['merchant_uid']
        order = Order.objects.get(order_number=merchant_uid)
        order.cancel_amount = response['cancel_amount']
        order.is_cancelled = True
        order.save()
        return {
            'result': order
        }
