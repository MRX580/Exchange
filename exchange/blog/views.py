from django.shortcuts import render
from .models import Blog


def index(request):
    get_blog = Blog.objects.all()
    return render(request, 'blog/index.html', {'data_blog': get_blog})


def blog(request, pk):
    get_blog = Blog.objects.get(pk=pk)
    return render(request, 'blog/blog.html', {'data_blog': get_blog})