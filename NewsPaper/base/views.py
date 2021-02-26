from django.shortcuts import render
#from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
# Create your views here.

from django.views.generic import ListView, DetailView ,UpdateView, CreateView, DeleteView # импортируем класс получения деталей объекта
from .models import Post
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-time_posted')


# создаём представление в котором будет детали конкретного отдельного товара
class PostDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'post.html'  # название шаблона будет product.html
    context_object_name = 'post'  # название объекта. в нём будет

class SearchPosts(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-time_posted']

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context
class Posts(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-time_posted']
    paginate_by = 10  # поставим постраничный вывод в один элемент

    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())


        context['form'] = PostForm()
        return context

    #def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST запроса

        #if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
            #form.save()

        #return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(CreateView):
    template_name = 'post_edition/post_create.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdateView(UpdateView):
    template_name = 'post_edition/post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'post_edition/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
#def handler404(request, *args, **argv):
    #response = render('404.html', {},
                                  #context_instance=RequestContext(request))
    #response.status_code = 404
    #return response