
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('articals', views.ArticalViewset, basename='articals')
router.register('users', views.UserViewset, basename='users')


urlpatterns = [
    # path('', views.Index , name='index' ),
    
    #-------Function Base APIs view urls--------
    # path('articals/', views.artical_list, name='articals' ),
    # path('articals/<int:pk>/', views.artical_detail, name='artical_detail' )
    
        
    #----------by using the Class Based API Views & Generic APIView & Mixins ------------
    
    # path('articals/', views.ArticalsList.as_view(), name='articalsList'),
    # path('articals/<int:id>/', views.ArticalDetail.as_view(), name='articalsDetail'),
    
    
    # -------------By using the Generic, Model and ViewSet & Router  ------------------
    path('api/', include(router.urls)),
    
    
    
]
