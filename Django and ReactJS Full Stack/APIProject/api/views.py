from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Artical
from .serializers import ArticalSerializer ,UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework import generics , mixins , viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
# Create your views here.





#       --------------------- Start Model Viewsets  -----------------------
 
class ArticalViewset(viewsets.ModelViewSet):
    queryset = Artical.objects.all()
    serializer_class = ArticalSerializer
    
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    
    
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)    
    
    
    
    
    

#       --------------------- End Model Viewsets  -----------------------

#  ---------- Start Function Base Views ----------
'''

@api_view(['GET', 'POST'])
def artical_list(request):
    
    if request.method == 'GET':
        articals = Artical.objects.all()
        serializer = ArticalSerializer(articals, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = ArticalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def artical_detail(request, pk):
    try:
        artical = Artical.objects.get(pk=pk)
    except Artical.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ArticalSerializer(artical)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArticalSerializer(artical, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        artical.delete()
        return HttpResponse(status=204)
    

'''
    # -----------END Function base view  ------------




#   ------------Start Class Bawe APi View --------------------
'''


class ArticalsList(APIView):
    def get(self, request):
        articals = Artical.objects.all()
        serializer = ArticalSerializer(articals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ArticalDetail(APIView):
    def get(self, request, id):
        artical = Artical.objects.get(id=id)
        serializer = ArticalSerializer(artical)
        return Response(serializer.data)
    def get_object(self, id ):
        try:
            return Artical.objects.get(id=id)
        except Artical.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        artical = self.get_object(id)
        serializer = ArticalSerializer(artical, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        artical = self.get_object(id)
        artical.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    #   ------------Class Bawe APi View End--------------------

'''
#       --------------------- End Class Bawe APi View -----------------------

#       --------------------- BY Using the Generic & MIXINS -----------------------

'''
class ArticalsList(generics.GenericAPIView, mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   ):
    queryset = Artical.objects.all()
    serializer_class = ArticalSerializer
    
    def get(self, reqeust):
        return self.list(reqeust)
    def post(self, request):
        return self.create(request)
    
class ArticalDetail(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Artical.objects.all()
    serializer_class = ArticalSerializer
    lookup_field = 'id'
    
    def get(self, request,id):
        return self.retrieve(request , id)
    def put(self, request, id):
        return self.update(request ,id)
    def delete(self,request, id):
        return self.destroy(request , id)
    

'''    
#       --------------------- End the Generic & MIXINS -----------------------
    
    
#       --------------------- Start Viewsets and Routers -----------------------
'''
class ArticalViewset(viewsets.ViewSet):
    def list(self,reqeust):
        articals = Artical.objects.all()
        serializer = ArticalSerializer(articals, many=True)
        
        return Response(serializer.data)
    def create(self,request):
        serializer = ArticalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        queryset = Artical.objects.all()
        artical = get_object_or_404(queryset, pk=pk)
        serializer = ArticalSerializer(artical)
        return Response(serializer.data)
    def update(self, request, pk=None):
        artical = Artical.objects.get(pk=pk)
        serializer = ArticalSerializer(artical, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        artical = Artical.objects.get(pk=pk)
        artical.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''

#       --------------------- END Viewsets and Routers -----------------------
    
    
    
#       --------------------- Start  Generic Viewsets   -----------------------
'''
class ArticalViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin
                    ):
    queryset = Artical.objects.all()
    serializer_class = ArticalSerializer
    
    
'''     
#       --------------------- End Generic Viewsets  -----------------------









