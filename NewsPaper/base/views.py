from django.shortcuts import render
#from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
# Create your views here.

from django.views.generic import TemplateView, ListView, DetailView ,UpdateView, CreateView, DeleteView,View # импортируем класс получения деталей объекта
from .models import Post,Author,User,Category
from .filters import PostFilter, CategoryFilter
from .forms import PostForm,CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


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

class CategoriesList(ListView):
    model = Category
    template_name = 'categories/categories.html'
    context_object_name = 'categories'
    ordering = ['-id']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        not_subscribed = False
        if (Category.objects.filter(subscriber = self.request.user.id).exists()):
            not_subscribed = True
        context['not_subscriber'] = not_subscribed
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        cat = get_object_or_404(Category, id = request.POST.get('category_id'))
        id= cat.id
        if "subscribe" in self.request.POST.keys():

            Category.objects.get(pk=id).subscriber.add(user)
        return redirect('/')
    #def get(self, request, *args, **kwargs):
        #return render(request, 'categories/categories.html', {})


    #queryset = Category.objects.order_by('-id')


    #def get_context_data(self,
                         #**kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        #context = super().get_context_data(**kwargs)
        #context['filter'] = CategoryFilter(self.request.GET,
                                         #queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        #return context

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


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin,CreateView):
    permission_required = ('base.add_post')
    template_name = 'post_edition/post_create.html'
    form_class = PostForm

# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin,UpdateView):
    #login_url = 'accounts/login/'
    permission_required = ('base.change_post')
    template_name = 'post_edition/post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = ('base.delete_post')
    template_name = 'post_edition/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class AccountView(LoginRequiredMixin,TemplateView):
    model = User

    template_name = 'base.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class SubscribeView(LoginRequiredMixin,TemplateView):
    model = Category
    template_name = 'categories/finish_subscribe.html'
    context_object_name ='category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        not_subscribed = False
        if (Category.objects.filter(subscriber = self.request.user.id).exists()):
            not_subscribed = True
        context['not_subscriber'] = not_subscribed
        return context

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author.objects.create(user = user)
    return redirect('/')

@login_required
def subscribe(request):
    user = request.user
    category = Category.objects.get(id= request.GET)
    category.subscriber.add(user)
    return redirect('/')

class Subscribe(LoginRequiredMixin, CreateView):
    model = Category
    ordering_by = ['-id']
    context_object_name = 'categories'
    template_name = 'categories/subscribe.html'
    form_class = CategoryForm

    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.add(user)
        return redirect('/')

class CategoryAdd(CreateView):
    template_name = 'categories/subscribe.html'
    model = Category
    ordering_by = ['']
    context_object_name = 'categories'
    queryset = Category.objects.all()
    form_class = CategoryForm

    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.add(user)
        return redirect('/')
#def handler404(request, *args, **argv):
    #response = render('404.html', {},
                                  #context_instance=RequestContext(request))
    #response.status_code = 404
    #return response

