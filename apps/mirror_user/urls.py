from django.urls import path
from . import views
app_name = 'mirror_user'
urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('register/', views.user_register, name="user_register"),
    path('logout/', views.user_logout, name="user_logout"),
    path("register_terms/", views.user_registerterms, name="user_registerterms"),
    path("forget_password/", views.user_forgetpassword, name="user_forgetpassword"),
    path("recover_password/", views.user_recoverpassword, name="user_recoverpassword"),
]
