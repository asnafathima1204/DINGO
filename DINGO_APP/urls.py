from django.urls import path
from DINGO_APP import views

urlpatterns = [
    # path('', views.my_first_view, name='myfirstview')
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('chefs/',views.chefs,name='chefs'),
    path('blog/',views.blog,name='blog'),
    path('elements/', views.elements, name='elements'),
    path('food_menu/', views.food_menu, name='food_menu'),
    path('single-blog/',views.single_blog,name='single-blog'),
    path('contact/',views.contact,name='contact'),
    path('cart/',views.cart,name='cart'),
    # signup/login/logout
    path('signup/',views.user_registration,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),

    path('home/',views.user_home,name='user_home'),
    path('order/', views.user_order, name='user_order'),
    path('invoice/', views.user_invoice, name='user_invoice'),
    path('checkout_view/', views.checkout_view, name='checkout_view'),
    path('profile/', views.user_profile, name='user_profile'),
    path('save_address/', views.save_address, name='save_address'),
    path('update_address/<int:id>/', views.update_address, name='update_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('item_filter/<str:category>/', views.item_filter, name='item_filter'),
    path('add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path('increment_quantity/<int:id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:id>/', views.decrement_quantity, name='decrement_quantity'),
    path('update_size/<int:id>/', views.update_size, name='update_size'),
    path('remove_cart/<int:id>/', views.remove_cart, name='remove_cart'),
    # path('order_details/<int:id>/', views.order_details, name='order_details'),
    path('change_address/', views.change_address, name='change_address'),



   #admin dashboard
    path('dashboard/',views.dashboard,name='dashboard'),
    path('admin_fooditems', views.admin_fooditems, name='admin_fooditems'),
    path('admin_viewitems/<int:id>/', views.admin_viewitems, name='admin_viewitems'),
    path('admin_additems', views.admin_additems, name='admin_additems'),
    path('admin_edititems/<int:id>/', views.admin_edititems, name='admin_edititems'),
    path('admin_deleteitems/<int:id>/', views.admin_deleteitems, name='admin_deleteitems'),
    path('admin_order', views.admin_order, name='admin_order'),
    path('admin_user', views.admin_user, name='admin_user'),


]
