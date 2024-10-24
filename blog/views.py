from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# gera uma lista de instâncias
class BlogListView(ListView):
    model = Post
    template_name = "home.html"

# gera uma única instância do objeto
class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
