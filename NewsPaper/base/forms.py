from django import forms
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
        fields = ['name','subscriber']

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=False)

class PersonForm(forms.Form):
	first_name = forms.CharField()

class ContactFormPWithPriority(ContactForm, PersonForm):
	priority = forms.CharField()
	cc_myself = None
	# prefix = 'person'
