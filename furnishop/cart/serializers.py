from rest_framework import serializers
from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items_count']

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_total_items_count(self, obj):
        return obj.get_total_items_count()


# AddCartItemSerializer-ით ვიღებ მონაცემებს (product_id და quantity) POST მეთოდით
class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

# Browsable API-ში ფორმა გამოჩნდეს remove-ისთვის, რომელსაც მხოლოდ
class RemoveCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
