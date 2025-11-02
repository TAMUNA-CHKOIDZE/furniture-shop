# FilterSet-ის გადატვირთვა, რადგან choices-დან IntegerField-ების (color, material) ტექსტურად ჩაწერა შეძლოს მომხმარებელმა URL-ში ფილტრაციისას,
# ასევე category-ის slug-ის მიხედვით ჩაწერა შეძლოს: GET /api/products/?color=white&material=wood&category=table
from django_filters import rest_framework as filters

from products.choices import COLOR_CHOICES, MATERIAL_CHOICES
from products.models import Product


class ProductFilter(filters.FilterSet):
    # ფერის ტექსტური ფილტრი
    color = filters.CharFilter(method='filter_color')
    # მასალის ტექსტური ფილტრი
    material = filters.CharFilter(method='filter_material')
    # კატეგორიის slug–ის მიხედვით ფილტრი
    category = filters.CharFilter(field_name='category__slug', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category', 'color', 'material']

    # ფერის ტექსტური ფილტრი
    def filter_color(self, queryset, name, value):
        mapping = {v.lower(): k for k, v in COLOR_CHOICES}
        key = mapping.get(value.lower())
        if key:
            return queryset.filter(color=key)
        return queryset.none()

    # მასალის ტექსტური ფილტრი
    def filter_material(self, queryset, name, value):
        mapping = {v.lower(): k for k, v in MATERIAL_CHOICES}
        key = mapping.get(value.lower())
        if key:
            return queryset.filter(material=key)
        return queryset.none()