from django.shortcuts import render
from django_filters import rest_framework as filters
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from .models import Order, OrderProduct
from ..review.models import Review
from .serializers import OrderSerializer, OrderUpdateSerializer, OrderProductUpdateSerializer
from .filters import OrderFilter, OrderProductFilter
from ..common.permissions import IsStaff, IsOwner
from .permissions import OrderProductPermission


has_review_subquery = Review.objects.filter(order_product=OuterRef('id'))

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset = OrderProduct.objects.annotate(has_review = Exists(has_review_subquery)))
    )
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter
    # permission_classes = [IsStaff]


class OrderDetailUpdateDeleteView(RetrieveUpdateAPIView):
    queryset = Order.objects.all().prefetch_related(
        Prefetch("order_products", queryset = OrderProduct.objects.annotate(has_review = Exists(has_review_subquery)))
    )
    serializer_class = OrderUpdateSerializer
    # permission_classes = [IsOwner]


class OrderProductDetailUpdateView(RetrieveUpdateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductUpdateSerializer
    # permission_classes = [OrderProductPermission]