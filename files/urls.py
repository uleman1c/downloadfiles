

from django.urls import path, include

from files import views

urlpatterns = [
    path('files/<slug:slug>', views.files),
]
