from django.shortcuts import render
from rest_framework import generics, mixins , permissions, authentication
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsStaffEditorPermissions

# Create your views here.


class ProductDetailViewAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
        
product_detail_view = ProductDetailViewAPI.as_view()

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self , serializer):
        instance = serializer.save()
        if not instance.content:
            instance.context = instance.title
product_update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
        
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
    
product_destroy_view = ProductDestroyAPIView.as_view()
    
class ProductListCreateViewAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsStaffEditorPermissions]
    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            contet = title
        serializer.save(content=content)
product_list_create_view = ProductListCreateViewAPI.as_view()

# class ProductListViewAPI(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
# product_list_view = ProductListViewAPI.as_view()




# All the CRUD opertaions are performed in this class base viwe withe including the functions of get and  post
#Start ProductMixinView

# class ProductMixinView(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin, #Same the generic Views
#     mixins.DestroyModelMixin, #Same the generic Views
#     generics.GenericAPIView,
# ):
    
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     def get(self, request, *arg, **kwargs):
#         pk = kwargs.get("pk")
#         if pk is not None:
#             return self.retrieve(request, *arg,**kwargs)
        
#         return self.list(request, *arg,**kwargs)
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# product_mixin_view = ProductMixinView.as_view()

# end ProductMixinView




@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None ,*args, **kwargs):
    if request.method == "GET":
        #Detail view
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # List of view
        else:
            queryset = Product.objects.all()
            data = ProductSerializer(queryset, many=True).data
            return Response(data)
    if request.method == "POST":
        #Create Item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            
            if content is None:
                contet = title
            serializer.save(content=content)
            # serializer.save()
            print(serializer.data)
            return Response(serializer.data)        
    return Response({"invalid":"Not good data"}, status=400)

