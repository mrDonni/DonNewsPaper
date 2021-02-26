from django_filters import FilterSet,IsoDateTimeFilter
from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'name': ['icontains'],
            'time_posted': ['date__gt'],
            'author__user': ['exact']
        }
