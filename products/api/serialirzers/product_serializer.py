from django.db import models
from products.models import Product
from rest_framework import serializers
from products.api.serialirzers.general_serializares import MeasureSerializer, CategoryProductSerializer


from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result
    return inner_func

@query_debugger
def xxx():
    queryset = Product.objects.select_related('measure_unit').all
    products = []
    for product in queryset:
        products.append({'id': product.id, 'name': product.name, 'publisher': product.measure_unit.description})
        
    return products

    
class ProductSerializer(serializers.ModelSerializer):
    #measure_unit = MeasureSerializer() # metodo 1
    #category_product = serializers.StringRelatedField() # metodo 2
        
    class Meta:
        model = Product
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'image': instance.image if instance.image != '' else '',
            'measure_unit': instance.measure_unit.description if instance.measure_unit is not None else '', # metodo 3
            'category_product': instance.category_product.description if instance.category_product is not None else '', # metodo 3
        }
