from django.urls import path
from . import views
from django.contrib.auth import views as log_views
from django.contrib.auth.views import ( PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, )
from .views import equipment_list, equipment_list_sorted, equipment_list_sorted_desc, equipment_list_sorted_user, equipment_list_sorted_user_desc,login_unauthorized,borrow_equipment, reservation_list_sorted, reservation_list_sorted_desc


urlpatterns = [
    
    #General web pages
    path('', views.home, name='home'),
    path('blist/', views.blist),
    path('navbar/', views.navbar),
    path('login/', log_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin_login/', log_views.LoginView.as_view(template_name='admin_login.html'), name='admin_login'),
    path('sign_up/', views.user_sign_up, name='sign_up'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('contactus/', views.contact_us, name='contact_page'),
    path('export_equipments_csv/', views.export_equipments_csv, name='export_equipments_csv'),
    path('export_bookings_csv/', views.export_bookings_csv, name='export_bookings_csv'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'), 
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('devicesInventory/sort/', equipment_list_sorted, name='devices_inventory_sorted'),
    path('devicesInventory/sortDesc/', equipment_list_sorted_desc, name='devices_inventory_sorted_desc'),
    path('devices/sort/', equipment_list_sorted_user, name='devices_inventory_user_sorted'),
    path('devices/sortDesc/', equipment_list_sorted_user_desc, name='devices_inventory_user_sorted_desc'),
    path('reservationInventory/sort/', reservation_list_sorted, name='reservation_list_sorted'),
    path('reservationInventory/sortDesc/', reservation_list_sorted_desc, name='reservation_list_sorted_desc'),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("login_unauthorized/", views.login_unauthorized,name = "login_unauthorized"),
    path("borrowEquipment/", views.borrow_equipment, name="borrow_equipment"),
    path("returnEquipment/", views.returnEquipment, name="return_equipment"),
    
    #Admin web pages
    path('mainAdmin/', views.main_admin, name='mainAdmin'),
    path('manageBookings/', views.manageBookings, name='manageBookings'),
    path('manageUsers/', views.manageUsers, name='manageUsers'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('updateProduct/', views.updateProduct, name='updateProduct'),
    path('devicesInventory/', views.devicesInventory, name='devicesInventory'),
    path('productOverview/', views.productOverview, name='productOverview'),
    path('productOverview2/', views.productOverview2, name='productOverview2'),
    path('productOverview3/', views.productOverview3, name='productOverview3'),
    path("completedBookingsAdmin/", views.completedBookingsAdmin, name="completedBookingsAdmin"),
    path("export_completed_bookings_admin/", views.export_completed_bookings_admin, name="export_completed_bookings_admin"),
    path("completedBookings/sortAZ/", views.completed_bookings_sorted_admin, name="completed_bookings_sorted_admin"), 
    path("completedBookings/sortZA/", views.completed_bookings_sorted_desc_admin, name="completed_bookings_sorted_desc_admin"),
    
    #User web pages
    path('mainUser/', views.main_user, name='mainUser'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('devices/', views.devices, name='devices'),
    path('currentBookings/', views.currentBookings, name='currentBookings'),
    path('updateAccountInformation/', views.updateAccountInformation, name='updateAccountInformation'),
    path('devicesInventoryUser/', views.devicesInventoryUser, name='devicesInventoryUser'),
    path('bookingsHistory/', views.bookingsHistory, name='bookingsHistory'),
    path('productOverview/', views.productOverview, name='productOverview'),
    path('productOverview2/', views.productOverview, name='productOverview2'),
    path('productOverview3/', views.productOverview, name='productOverview3'),
    path("borrowEquipmentUser/", views.borrowEquipmentUser, name="borrowEquipmentUser"),
    path("returnEquipmentUser/", views.returnEquipmentUser, name="returnEquipmentUser"),
    path("completedBookingsUser/", views.completedBookingsUser, name="completedBookingsUser"),
    path("completedBookings/sortAZUser/", views.completed_bookings_sorted_user, name="completed_bookings_sorted_user"), 
    path("completedBookings/sortZAUser/", views.completed_bookings_sorted_desc_user, name="completed_bookings_sorted_desc_user"),
    path("export_completed_bookings_user/", views.export_completed_bookings_user, name="export_completed_bookings_user"),
    path("export_current_bookings_user/", views.export_current_bookings_user, name="export_current_bookings_user"),
    path("export_booking_history_user/", views.export_booking_history_user, name="export_booking_history_user"),
    
    
    
    
]   
