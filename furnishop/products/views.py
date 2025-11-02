from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from products.filters import ProductFilter
from products.models import Product
from products.serializers import ProductSerializer


# ყველა პროდუქტის ვიუ (ლისტინგი)
class ProductListView(generics.ListAPIView):
    # API-ის მიერ დაბრუნებული მონაცემები იქნებიან ყველა Product ობიექტი ბაზაში, თუმცა მხოლოდ ისინი გამოჩნდება რომლებიც ხელმისაწვდომია
    queryset = Product.objects.filter(is_available=True)
    # მონაცემები ProductSerializer-ის მეშვეობით გადაიყვანება JSON ფორმატში, Serializer იღებს Product ობიექტებს და JSON-ის სახით უგზავნის მომხმარებელს.
    serializer_class = ProductSerializer
    # ფილტრაცია შესაძლებელია კატეგორიით, ფერით, მასალით
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter  # filterset-ის გადატვირთვა ფილტრის ლოგიკისთვის
    ordering_fields = ['price', 'created_at']  # დალაგება ფასის და შექმნის თარიღის მიხედვით ხდება

# კონკრეტული პროდუქტი
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



