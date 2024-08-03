# myapp/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import signup, index_view, login_view , verify_email  , logoutUser , profile_detail, change_password, home, search
 # template implementation
from .views import products, product_detail , cart , checkout , myAccount , wishlist , contactUs, products_by_category, order_confirmation, add_to_wishlist,remove_from_wishlist, products_by_brand



urlpatterns = [
    path('', home, name='home'),
    path('index/', index_view, name='index'),  

    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logoutUser/', logoutUser, name='logoutUser'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('profile-detail/', profile_detail, name='profile-detail'),
    # path('edit-profile/', editProfile, name='edit-profile'),
    path('change-password/',change_password, name='change-password'),
    path('search/', search, name='search'),

    # Template Implementation
    path('products/', products, name='products'),
    path('product_detail/<int:id>/', product_detail, name='product_detail'),
    path('products/category/<int:category_id>/', products_by_category, name='products_by_category'),
    path('products/brand/<int:brand_id>/', products_by_brand, name='products_by_brand'),
    path('cart', cart , name='cart'),
    path('checkout', checkout , name='checkout'),
    path('order-confirmation', order_confirmation, name='order_confirmation'),
    path('my-account', myAccount , name='my-account'),
    path('wishlist', wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/', remove_from_wishlist, name='wishlist_remove'),
    path('contactUs', contactUs, name='contactUs'),






] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)