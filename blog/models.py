from django.db import models
from django.urls import reverse

class Post(models.Model):
    autor = models.ForeignKey(  # relacionamento N-1
        "auth.User",
        on_delete=models.CASCADE
    )
    titulo = models.CharField(max_length=100)
    corpo = models.TextField()
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.titulo
        
    def get_absolute_url(self):  # usado no template para buscar a rota de um elemento da tabela
        return reverse("post_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("post_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("post_delete", kwargs={"pk": self.pk})

