from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Colecao 
from rest_framework import status

class ColecaoTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password') 

    def test_create_colecao_associada_ao_usuario(self):
        response = self.client.post('/colecao/', {
            'nome': 'Minha Coleção',
            'descricao': 'Uma descrição de teste'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        colecao = Colecao.objects.get(nome='Minha Coleção')
        self.assertEqual(colecao.usuario, self.user) 


class PermissoesTestes(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='testuser', password='password')
        self.colecao = Colecao.objects.create(nome="Coleção Teste", descricao="Descrição", usuario=self.user)

    def test_editar_colecao_propria(self):
        response = self.client.put(f'/colecao/{self.colecao.id}/', {
            'nome': 'Coleção Editada',
            'descricao': 'Nova descrição'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.colecao.refresh_from_db()
        self.assertEqual(self.colecao.nome, 'Coleção Editada')

    def test_editar_colecao_de_outro_usuario(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.put(f'/colecao/{self.colecao.id}/', {
            'nome': 'Nome Invalido',
            'descricao': 'Descrição Invalida'
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deletar_colecao_propria(self):

        response = self.client.delete(f'/colecao/{self.colecao.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Colecao.DoesNotExist):
            Colecao.objects.get(id=self.colecao.id)

    def test_deletar_colecao_de_outro_usuario(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.delete(f'/colecao/{self.colecao.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestesSemAutenticacao(TestCase):

    def test_criar_colecao_sem_autenticacao(self):
        response = self.client.post('/colecao/', {
            'nome': 'Coleção Não Autenticada',
            'descricao': 'Descrição de teste'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editar_colecao_sem_autenticacao(self):
        colecao = Colecao.objects.create(nome="Coleção Teste", descricao="Descrição", usuario=self.user)
        
        response = self.client.put(f'/colecao/{colecao.id}/', {
            'nome': 'Nome Atualizado',
            'descricao': 'Descrição atualizada'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deletar_colecao_sem_autenticacao(self):
        colecao = Colecao.objects.create(nome="Coleção Teste", descricao="Descrição", usuario=self.user)

        response = self.client.delete(f'/colecao/{colecao.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ListagemColecoesTestes(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='testuser', password='password')

        self.colecao_user = Colecao.objects.create(nome="Coleção do Teste", descricao="Descrição", usuario=self.user)
        self.colecao_other = Colecao.objects.create(nome="Coleção de Outro Usuário", descricao="Descrição", usuario=self.other_user)

    def test_listar_colecao_propria(self):
        response = self.client.get('/colecao/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.colecao_user.nome, [colecao['nome'] for colecao in response.data])

    def test_nao_listar_colecao_de_outro_usuario(self):
        response = self.client.get('/colecao/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.colecao_other.nome, [colecao['nome'] for colecao in response.data])
