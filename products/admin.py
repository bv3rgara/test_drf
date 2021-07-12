from django.contrib import admin
from products.models import *


class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'category_product', 'measure_unit', 'image', 'state')

admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Indicator, )
admin.site.register(Product, ProductAdmin)
