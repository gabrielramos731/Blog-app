# Blog App

## Set Up inicial

- Criar o diretório do projeto `blog-app`
- iniciar um ambiente virtual
- Criar um app django `blog`
- Realizar a *migration* do banco de dados
- Atualizar as configurações de *settings*
    - Aplicações instaladas

## Models

De forma simplificada, cada usuário poderá possuir múltiplos posts, além de poder criar, alterar ou deletá-los. O ORM fornecido pelo framework Django foi utilizado para criar uma estrutura simples de post, apenas com referência ao usuário, título e corpo do post.

```python
class Post(models.Model):
    autor = models.ForeignKey(  # relacionamento N-1
        "auth.User",
        on_delete=models.CASCADE
    )
    titulo = models.CharField(max_length=100)
    corpo = models.TextField()

    def __str__(self):
        return self.autor, self.titulo

    def get_absolute_url(self):  # usado no template para buscar a rota de um elemento da tabela
        return reverse("post_detail", kwargs={"pk": self.pk})
```

## Admin

Precisamos fazer com que a página de admin tenha acesso ao nosso modelo Post, para poder gerenciar de forma total esta tabela. Registramos então o modelo no arquivo *admin.py* da aplicação:

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

## Views

Configuramos as *views* para linkar os nossos *models* com os nossos *templates*. Para isso, foi criada uma view para listar todas instâncias do nosso modelo *Post* no template *home.html*  e uma segunda view que renderiza uma única instância baseado em sua pk*.*

```python
from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# gera uma lista de instâncias
class BlogListView(ListView):
    model = Post
    template_name = "home.html"
    
# gera uma única instância do objeto
class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
 
 # renderiza um template com campos para criar um novo post  
class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ['titulo','autor','corpo']
```

## URL’s

Direcionamos a URL base para que fosse tratada na aplicação blog. Na aplicação, definimos as rotas da URL com as views:

```python
# django_project > urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

# blog > urls.py
from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>', BlogDetailView.as_view(), name='post_detail'),
    path('post/new', BlogCreateView.as_view(), name='post_new'),
]
```

## Templates

Após estabelecer as rotas e relações das views com os modelos, podemos ter acesso às instâncias das tabelas relacionadas na view. Além disso, um template *base.html* é usado para reutilizar código (DRY), que é estendido por *home.html*.

Para facilitar o desenvolvimento da estilização das interfaces, realizamos a integração do Tailwind CSS com o framework Django, permitindo a estilização *utility first.* A documentação do *Django Tailwind* pode ser encontrada em: 

[Welcome to Django Tailwind’s documentation! — Django-Tailwind 2.0.0 documentation](https://django-tailwind.readthedocs.io/en/latest/index.html)

## Visão Geral

![image.png](/images/image.png)

A URL root chama a view *BlogListView,* que renderiza o template *home.html* com o modelo de dados *Post*. Podemos usar uma tag django *url* para chamar uma outra rota `"post_detail" post.pk`  que aciona a view *BlogDetailView,* renderizando o template *post_detail.html* juntamente ao modelo *Post.* Ambos templates citados, estendem de *base.html. CreateDetailView* é responsável por criar um novo post e atualizar *Post_model.* 

## Busca por post e posts por autor

![image.png](/images/image%201.png)

Ao preencher um formulário e submeter, os dados são enviados para a rota nomeada em *action* do form via URL e direcionado para a view BlogPostSearch desta rota, que se comunica com a tabela de PostModel para serem processados com base nos dados passados pelo GET. Os dados são retornados para serem renderizados no template *post_search.html.*

```python
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
```

## Autenticação

### Log In

Por padrão, o Django já nos fornece uma aplicação para serviços de autenticação de usuário `django.contrib.auth` , já fornecendo diversas views para tais tarefas.

Em *#django-project > urls.py,* adicionamos um caminho para processar as rotas relacionadas a autenticação `path('contas/', include("django.contrib.auth.urls"))` . A view *LoginView* irá buscar um template em *templates>registration>login.html* naturalmente, onde será renderizado os campos para login.

```html
*<!-- templates > registration > login.html -->*
<div>
    <h2>Log In</h2>
    <form method="post">{% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Log In</button>
    </form>
</div>
```

Podemos adicionar em *setings.py* uma nova linha que redireciona para uma URL após um login bem sucedido: `LOGIN_REDIRECT_URL = "home"`

### Log Out

Adicionamos apenas um form para enviar via POST uma requisição para deslogar para a rota correta.

```html
<form method="POST" action="{% url 'logout' %}">{% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

### Sign Up

Para o sistema de registrar-se, criamos uma nova aplicação *accounts* que irá gerenciar questões de Sign Up. Devemos indicar o arquivo dessas rotas e seu prefixo de acesso `path('contas/', include("accounts.urls"))`

```python
# accounts > urls.py
from .views import SignUpView
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup')
]

# accounts > views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
# templates > resgitration > signup.html
<div class='text-black'>
    <h2>Sign In</h2>
    <form method="post">{% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Sign In</button>
    </form>
</div>
```

Adicionamos a rota *signup* na aplicação para a view *SignUpView*, que cria o formulário *signup.html* de cadastro e retorna para *login* após sucesso.