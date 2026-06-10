from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list),
    path('posts/<int:pk>/like/', views.post_like),
    path('posts/<int:pk>/comments/', views.comment_create),
]
