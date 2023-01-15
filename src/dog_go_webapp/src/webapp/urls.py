from django.urls import include, path

from . import views
from django.contrib.auth.decorators import login_required
from django.contrib import admin


admin.autodiscover()
admin.site.login = login_required(admin.site.login)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('social_django.urls')),
    path('profile/', views.profile),
    path('logout/', views.logout),
]
