from django.urls import path
from DINGO_APP import views

urlpatterns = [
    # path('', views.my_first_view, name='myfirstview')
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('chefs/',views.chefs,name='chefs'),
    path('food_menu/', views.food_menu, name='food_menu'),
    path('contact/',views.contact,name='contact'),
    path('item_filter/<str:category>/', views.item_filter, name='item_filter'),
    path('exclusive_item/', views.exclusive_item, name='exclusive_item'),
    path('view_item/<int:id>/', views.view_item, name='view_item'),

    path('signup/',views.user_registration,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),

    path('home/',views.user_home,name='user_home'),
    path('cart/',views.cart,name='cart'),
    path('order/', views.user_order, name='user_order'),
    path('reservation/', views.user_reservation, name='user_reservation'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('cancel_reservation/<int:id>/', views.cancel_reservation, name='cancel_reservation'),
    path('invoice/<int:id>', views.user_invoice, name='user_invoice'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('profile/', views.user_profile, name='user_profile'),
    path('save_address/', views.save_address, name='save_address'),
    path('update_address/<int:id>/', views.update_address, name='update_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path('increment_quantity/<int:id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:id>/', views.decrement_quantity, name='decrement_quantity'),
    path('update_size/<int:id>/', views.update_size, name='update_size'),
    path('remove_cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('confirmation_page/', views.confirmation_page, name='confirmation_page'),
    path('buynow/<int:id>/', views.buy_now, name='buynow'),
    

   #admin dashboard
    path('dashboard/',views.dashboard,name='dashboard'),
    path('admin_fooditems/', views.admin_fooditems, name='admin_fooditems'),
    path('admin_viewitems/<int:id>/', views.admin_viewitems, name='admin_viewitems'),
    path('admin_additems/', views.admin_additems, name='admin_additems'),
    path('admin_edititems/<int:id>/', views.admin_edititems, name='admin_edititems'),
    path('admin_deleteitems/<int:id>/', views.admin_deleteitems, name='admin_deleteitems'),
    path('admin_order/', views.admin_order, name='admin_order'),
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    path('admin_vieworder/<int:id>/', views.admin_vieworder, name='admin_vieworder'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('toggle-status/<int:user_id>/',views.toggle_user_status, name='toggle_user_status'),
    path('admin_chef/',views.admin_chef, name='admin_chef'),
    path('admin_viewchef/<int:id>/',views.admin_viewchef, name='admin_viewchef'),
    path('admin_addchef/',views.admin_addchef, name='admin_addchef'),
    path('admin_editchef/<int:id>/',views.admin_editchef, name='admin_editchef'),
    path('admin_deletechef/<int:id>/',views.admin_deletechef, name='admin_deletechef'),
    path('admin_reservation/',views.admin_reservation, name='admin_reservation'),
    path('admin_contact/',views.admin_contact, name='admin_contact'),
]
handler404 = 'DINGO_APP.views.not_found'

