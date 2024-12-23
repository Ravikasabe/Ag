from django.conf.urls.static import static
from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    #---------------------------- All Users ---------------------------------
    path("", views.index, name='index'),
    path("main/",views.main, name="main"),
    path("products/",views.products, name="products"),
    path("about/",views.about, name="about"),
    path("contact/",views.contact, name="contact"),
    path('subscribe_all/', views.subscribe_all, name='subscribe_all'),
    #------------------------------------------------------------------------


    #--------------------------- Login / Register ----------------------
    path("login/",views.login , name="login"),
    path("register/",views.register, name="register"),
    #-------------------------------------------------------------------


    #------------------------------------------- Registered Users ----------------------------------------------------------
    path("main_user/",views.main_user, name="main_user"),
    path("profile/<int:user_id>/",views.profile, name="profile"),
    path('edit_pf/', views.edit_pf, name='edit_pf'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path("products_user/",views.products_user, name="products_user"),
    path('more_info/<str:product_type>/<int:product_id>/', views.moreinfo, name='more_info'),
    path('about_user/', views.about_user, name='about_user'),
    path("contact_user/",views.contact_user, name="contact_user"),
    path('subscribe_product/', views.subscribe_product, name='subscribe_product'),
    # User Cart 
    path('add-to-cart/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove_one_from_cart/<str:product_type>/<int:product_id>/', views.remove_one_from_cart, name='remove_one_from_cart'),
    path('buy/<str:item_total>/', views.buy, name='buy'),
    #--------------------------------------------------------------------------------------------------------------------------
    
    
    #-------------------------------------------- Admin ----------------------------------------------------
    path("Admin_page/",views.admin, name="Admin"),
    # Admin filter 
    path("filter_seed/",views.filter_seed, name="filter_seed"),
    path("filter_Fertilizer/",views.filter_Fertilizer, name="filter_Fertilizer"),
    path("filter_pesticide/",views.filter_pesticide, name="filter_pesticide"),
    path("filter_equipment/",views.filter_equipment, name="filter_equipment"),
    path("filter_feed/",views.filter_feed, name="filter_feed"),
    path("filter_tools/",views.filter_tools, name="filter_tools"),
    # Admin products 
    path("add_product/",views.add_product, name="add_product"),
    path('product_update/<str:product_type>/<int:product_id>/', views.update_product, name='product_update'),
    path('product_delete/<str:product_type>/<int:product_id>/', views.delete_product, name='product_delete'),
    # Admiin Users 
    path('admin_user/', views.admin_users, name='admin_user'),
    path('user_filter/', views.user_filter, name='user_filter'),
    path('user_update/<int:user_update_id>/', views.user_update, name='user_update'),
    path('make_superuser/<int:user_update_id>/', views.make_superuser, name='make_superuser'),
    path('remove_superuser/<int:user_update_id>/', views.remove_superuser, name='remove_superuser'),
    path('make_staff/<int:user_update_id>/', views.make_staff, name='make_staff'),
    path('remove_staff/<int:user_update_id>/', views.remove_staff, name='remove_staff'),
    path('user_delete/<int:user_del_id>/', views.user_delete, name='user_delete'),
    #-----------------------------------------------------------------------------------------------------------

    #--------------------- logout ----------------------
    path("logout/",views.user_logout, name="logout"),
    #----------------------------------------------------

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

