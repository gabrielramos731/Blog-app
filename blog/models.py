from django.db import models
from django.urls import reverse

class Post(models.Model):
    autor = models.ForeignKey(  # relacionamento N-1
        "auth.User",
        on_delete=models.CASCADE
    )
    titulo = models.CharField(max_length=100)
    corpo = models.TextField()

    def __str__(self):
        return self.titulo
        
    def get_absolute_url(self):  # ainda não sei o que é
        return reverse("post_detail", kwargs={"pk": self.pk})
