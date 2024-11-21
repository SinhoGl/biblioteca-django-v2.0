# Generated by Django 5.1 on 2024-11-20 21:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_autor_nome_alter_categoria_nome_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Colecao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('descricao', models.TextField(blank=True)),
                ('colecionador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colecoes', to=settings.AUTH_USER_MODEL)),
                ('livros', models.ManyToManyField(related_name='colecoes', to='core.livro')),
            ],
        ),
    ]
