from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static 
app_name = 'products'
urlpatterns = [
   path('', views.my_view, name = "my_view" ),
   path('api/', views.api_list, name = "api_list" ),
   path('cart-list/', views.cart_list, name = "cart_list" ),
   # path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
   path('delete-product/<pk>/',views.delete_product, name='delete_product'),
   path('update-product/<pk>/',views.update_product,name='update_product'),
   path('api/<pk>/',views.single_product,name='single_product'),
   path('cart/',views.cart_list,name='cart_list'),
   path('cart/<pk>/',views.single_cart,name='single_cart'),
   path('delete-cart/<pk>/',views.delete_cart,name='delete_cart'),
   path('update-cart/<pk>/',views.update_cart,name='update_cart'),
       
   ]
   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)