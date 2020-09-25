from django.urls import path
from . import views

app_name='signin'
urlpatterns = [
    path('',views.home,name="home"),
    path('header/',views.header,name="header"),
    path('signup_buyer/',views.signup_buyer,name="signup_buyer"),
    path('signup_seller',views.signup_seller,name="signup_seller"),
    path('login',views.loginview,name="login"),
    path('logout',views.logoutview,name='logout'),
    path('cityselection',views.cityselection,name='cityselection'),
    path('product/<int:cat_id>/',views.product,name='product'),
    path('product_filter/<int:subcat_id>/',views.product_filter,name='products_fltr'),
    path('addcart/<int:adv_id>/',views.addcart,name='addcart'),
    path('add_to_wishlist/<int:adv_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('product_detail/<int:adv_id>/',views.product_detail,name='product_detail'),
    path('profileview/',views.profileview,name='profileview'),
    path('profileedit',views.profileedit,name='profileedit'),
    path('profileview/change-password/',views.changePwd,name='chngPwd'),
    path('cart/',views.cart,name='cart'),
    path('cart/rem/<int:pk>/',views.cartAdvRemove,name='cartAdvRemove'),
    path('cart/fetch-dates/',views.fetch_booked_dates,name='fetch_booked_dates'),
    path('ordr/place/',views.saveOrdr,name='ordr_save'),
    path('ordrsummry/',views.ordrSummery,name='ordrSummery'),
    path('ordrsuccess/',views.ordrSuccess,name='ordrPlacedMsg'),
    path('ordr-receipt/<int:pk>/',views.odrReceipt,name='odr-receipt'),
    path('cpnvalidate/',views.validateCoupon,name='cpn_validate'),
    path('wishlist/',views.wishlist,name='wishlist')
]