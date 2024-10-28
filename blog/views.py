from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post

# gera uma lista de instâncias
class BlogListView(ListView):
    model = Post
    template_name = "home.html"

# gera uma única instância do objeto
class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ['titulo','autor','corpo','tag']
    
class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ['titulo','corpo', 'tag']
    
class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home") # redireciona para após rota até terminar de deletar

class PostTitleSearchListView(ListView):
    model = Post
    template_name = "home.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(titulo__icontains=query)
    
class PostAuthorSearchListView(ListView):
    model = Post
    template_name = "home.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(autor__username__icontains=query)

class PostTagListView(ListView):
    model = Post
    template_name = "home.html"

    def get_queryset(self):
        query = self.request.GET.get('tag')
        return Post.objects.filter(tag=query)
    