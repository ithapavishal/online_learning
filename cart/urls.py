from django.urls import path
from .views import *
urlpatterns = [
    path('cart/add/<int:course_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:cart_item_id>/',
         remove_from_cart, name='remove_from_cart'),
    # payment form
    path('payement_form/<int:cartItem_id>/',
         payement_form, name='payement_form'),

    #  payment
    path('init_khalti/<int:id>/', init_khalti, name='init_khalti'),
    path('verify/', verify_khalti, name='verify_khalti'),
]
