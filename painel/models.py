from django.db import models

# Create your models here.

#Criando a model para salvar o pedido no banco de dados. 

class Pedido(models.Model):
    usuario = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
