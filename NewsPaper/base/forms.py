from django.forms import ModelForm
from .models import Post,Category


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['name', 'type', 'author', 'category','text']

class CreatePostForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['name', 'type',  'category','text']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'subscriber']