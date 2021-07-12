from base.api import GeneralListAPIView
from products.api.serialirzers.general_serializares import MeasureSerializer, IndicatorSerializer, CategoryProductSerializer

class MeasureUnitListAPIView(GeneralListAPIView):
    serializer_class = MeasureSerializer


class CategoryProductListAPIView(GeneralListAPIView):
    serializer_class = CategoryProductSerializer


class IndicatorListAPIView(GeneralListAPIView):
    serializer_class = IndicatorSerializer

