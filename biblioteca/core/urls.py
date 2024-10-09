from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('livros/', views.LivroList.as_view(), name='livros-list'),
    path('livro/<int:pk>/', views.LivroDetail.as_view(), name='livro-detail'),
]