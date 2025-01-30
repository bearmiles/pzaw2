from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("<str:club_name>", views.club_detail, name="club_detail"),
#     path("<int:id>/", views.by_id, name="by_id"),
#     path("<str:club_n>/", views.by_name, name="by_name"),
]
