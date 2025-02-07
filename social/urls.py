from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("club/<str:club_name>", views.club_detail, name="club_detail"),
    path("login/", views.loginn, name="loginn"),
    path("signup/", views.signup, name="signup"),
]
