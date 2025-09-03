from django.urls import path
from . import views

urlpatterns = [
    path('my-view/', views.my_view, name='my_view'),
    path('limited-authenticated/', views.limited_authenticated_view, name='limited_authenticated'),
    path('limited-anonymous/', views.limited_anonymous_view, name='limited_anonymous'),
    path('login/', views.login_view, name='login'),
]
