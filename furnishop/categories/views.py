from rest_framework import generics

from categories.models import Category
from categories.serializers import CategorySerializer


# ყველა კატეგორია
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# კონკრეტული კატეგორია
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
