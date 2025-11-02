from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    # ეს ქმნის ჩაშენებულ serializer-ს (nested serializer) ანუ როდესაც პროდუქტის მონაცემებს წამვოიღებ API-დან (GET),
    # category ველში ავტომატურად გამოვა კატეგორიის სრული ინფორმაცია, არა მხოლოდ id
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    # მეთოდები JSON-ში ინტეჯერის ნაცვლად color-ის და material-ის ტექსტური მნიშვნელობებისთვის
    color = serializers.SerializerMethodField()
    material = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_id', 'description', 'price', 'stock',
            'color', 'material', 'is_available', 'featured', 'created_at', 'updated_at',
            'product_image', 'product_image2', 'product_image3', 'product_image4'
        ]

    def get_color(self, obj):
        return obj.get_color_display()

    def get_material(self, obj):
        return obj.get_material_display()
