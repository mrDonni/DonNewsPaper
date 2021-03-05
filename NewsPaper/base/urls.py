from django.urls import path,include
from .views import * # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', Posts.as_view()),
    path('<int:pk>/', PostDetail.as_view(),name='post_detail'),
    path('search/', SearchPosts.as_view()),
    path('add/',PostCreateView.as_view(),name='post_create'),
    path('<int:pk>/edit/',PostUpdateView.as_view(),name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(),name="post_delete"),
    path('userdata/<int:pk>', AccountView.as_view(), name = "user_data")

    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
]
#handler404 = 'base.views.handler404'
