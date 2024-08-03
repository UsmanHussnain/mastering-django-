from django.urls import path 
from .views import home, adminIndex,productList, uiElements,tabPanel, charts, table, forms, blankpage, adminLogin, adminLogout, create_Super_User
from .views import add_product, edit_product, product_detail   , add_product_images_view, delete_product, adminOrder, edit_order, category_detail, delete_category , brand_detail, delete_brand, list_querries, delete_querry
urlpatterns = [
   path('', home , name = 'home'),
   path('adminIndex',adminIndex  , name = 'adminIndex'),
   path('uiElements',uiElements  , name = 'uiElements'),
   path('productList',productList  , name = 'productList'),
   path('tabPanel',tabPanel  , name = 'tabPanel'),
   path('charts',charts  , name = 'charts'),
   path('table',table  , name = 'table'),
   path('forms',forms  , name = 'forms'),
   path('blankpage',blankpage  , name = 'blankpage'),
   path('adminLogout',adminLogout  , name = 'adminLogout'),
   path('adminLogin',adminLogin  , name = 'adminLogin'),
   path('create-superuser',create_Super_User  , name = 'create-superuser'),


   path('add-product',add_product  , name = 'add-product'),
   path('edit-product/<int:pk>/', edit_product, name='edit-product'),
   path('product-detail/<int:pk>',product_detail  , name = 'product-detail'),
   path('addimage/<int:pk>/',add_product_images_view, name="addimage"),
   path('product/<int:pk>/delete/', delete_product, name='product-delete'),
   path('adminOrder',adminOrder , name = 'adminOrder'),
    path('orders/edit/<int:order_id>/', edit_order, name='edit_order'),
    path('category-detail/', category_detail , name='category-detail'),
    path('deleteCategory/<int:category_id>/', delete_category, name='delete-category'),
    path('brand-detail/', brand_detail , name='brand-detail'),
    path('deleteBrand/<int:brand_id>/', delete_brand, name='delete-brand'),
    path('querries/', list_querries, name='querries'),
    path('delete-querry/<int:pk>/', delete_querry, name='delete-querry'),
   
   
    

] 
