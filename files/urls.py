

from django.urls import path, include, re_path

from files import views

urlpatterns = [
    path('files/<slug:slug>', views.files),
    path('files/<slug:slug>=<str:mode>', views.filesd),
    path('gfbp/', views.gfbp),]
