from django.db import models


class Conversa(models.Model):
    usuario = models.CharField(max_length=100)
    mensagem = models.TextField()
    resposta = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.mensagem[:30]}"