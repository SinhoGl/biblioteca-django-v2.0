from .filters import LivroFilter
from rest_framework import generics, permissions
from .models import Livro, Categoria, Colecao
from .serializers import LivroSerializer, CategoriaSerializer, ColecaoSerializer
from .custom_permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

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
    
class ColecaoListCreate(generics.ListCreateAPIView):
    # view para listar e criar colecoes
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(colecionador=self.request.user)
        
class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    # recuperar, atualizar e deletar uma colecao
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return[permissions.IsAuthenticated(), IsOwner()]
        return [permissions.AllowAny()]
    
class HomeView(generics.ListAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer