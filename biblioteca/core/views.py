from .filters import LivroFilter
from rest_framework import generics
from .models import Livro, Categoria
from .serializers import LivroSerializer, CategoriaSerializer


class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filterset_class = LivroFilter
    ordering_fields = ['titulo', 'autor', 'categoria', 'publicado_em']
    
class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

  
class CategoriaListCreate(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    ordering_fields = ["^name",]

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class HomeView(generics.ListAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer