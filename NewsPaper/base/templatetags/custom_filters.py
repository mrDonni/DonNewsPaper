from django import template

register = template.Library()  # если мы не зарегестрируем наши фильтры,
# то django никогда не узнает где именно их искать и фильтры потеряются(

@register.filter(name = 'strong_language')
def strong_language(value):
    words = ['Пиздец','Хуй','Жопа','Нигер']
    for x in words:
        x = str(x)
        if x.lower()  in str(value.lower()):
           value = value.replace(x.lower(),"***").replace(x.title(),'***')
    return value
