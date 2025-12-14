from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # App routes
    path('', include('dashboard.urls')),

    # Auth routes (NO dashboard view imports here)
    path(
        'login/',
        auth_views.LoginView.as_view(template_name="dashboard/login.html"),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
]
