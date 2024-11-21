from rest_framework import serializers
from .models import Categoria, Autor, Livro, Colecao


class CategoriaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        return Categoria.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.save()
        return instance
class AutorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        return Autor.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.save()
        return instance
    
class LivroSerializer(serializers.Serializer):
    '''identificadores dos livros'''
    id = serializers.IntegerField(read_only=True)
    titulo = serializers.CharField(max_length=200)
    autor = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all())
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    publicado_em = serializers.DateField()
    
    def create(self, validated_data):
        return Livro.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.autor = validated_data.get('autor', instance.autor)
        instance.categoria = validated_data.get('categoria',
    instance.categoria)
        instance.publicado_em = validated_data.get('publicado_em',
    instance.publicado_em)
        instance.save()
        return instance

class ColecaoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=120)
    descricao = serializers.CharField(required=False, allow_blank=True)
    livros = serializers.PrimaryKeyRelatedField(
        queryset=Livro.objects.all(),
        many = True
    )
    colecionador = serializers.PrimaryKeyRelatedField(read_only= True)
    
    def create(self, validated_data):
        #metodo para criar um nova instancia de colecao
        livros = validated_data.pop('livros', [])
        colecao = Colecao.objects.create(**validated_data)
        colecao.livros.set(livros) 
        return colecao
    
        #metodo para atualizasr uma instancia existente de colecao   
    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        
        livros = validated_data.get('livros', None)
        if livros is not None:
            instance.livros.set(livros)
        
        instance.save()
        return instance