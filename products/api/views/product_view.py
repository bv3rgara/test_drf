from rest_framework import generics, serializers, status, viewsets
from rest_framework.response import Response
from base.api import GeneralListAPIView
from products.api.serialirzers.product_serializer import ProductSerializer
from products.models import Product
from users.authentication_mixins import Authentication


class ProductListAPIView(GeneralListAPIView):
    serializer_class = ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Producto creado!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# devuelve una unica instancia
class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    #def get(self, request, pk=None):
        #para obtener el pk directamente sobreescribimos el def get


class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def delete(self, request, pk=None):
        # no realizamos update directamente para tener control en los status messages
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({"message": "Producto eliminado!"}, status=status.HTTP_200_OK)
        return Response({"message": "Producto no encontrado!"}, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self, pk):
        return self.get_serializer().Meta.model.objects.filter(state=True).filter(id=pk).first()

    #metodo para obtener la instancia
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Producto no encontrado!"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = serializer_class().Meta.model.objects.filter(state=True)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Producto creado!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class().Meta.model.objects.filter(state='True')
        else:
            return self.serializer_class().Meta.model.objects.filter(state='True', id=pk).first()

    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Producto no encontrado!"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        print(request.data, "-------------------------------*******")
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("NOOOOOOOOOOOOOOOOOOOOO")
    
    def delete(self, request, pk=None):
        # no realizamos update directamente para tener control en los status messages
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({"message": "Producto eliminado!"}, status=status.HTTP_200_OK)
        return Response({"message": "Producto no encontrado!"}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    #queryset = ProductSerializer.Meta.model.objects.filter(state='True')

    def get_queryset(self, pk=None):
        return self.serializer_class().Meta.model.objects.filter(state='True')

    """
    def list
    def create
    def retrieve
    def update
    def partial_update
    def destroy
    """