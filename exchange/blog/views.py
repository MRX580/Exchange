from django.shortcuts import render
from .models import Blog
from .forms import BlogForm
from django.contrib import messages
from django.core.exceptions import ValidationError


def index(request):
    get_blog = Blog.objects.all()[::-1]
    return render(request, 'blog/index.html', {'data_blog': get_blog})


def blog(request, pk):
    get_blog = Blog.objects.get(pk=pk)
    return render(request, 'blog/blog.html', {'data_blog': get_blog})


def create_blog(request):
    if not request.user.is_staff:
        raise ValidationError('Шо?')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.save()
            name.save()
            messages.success(request, 'Блог был успешно опубликован!')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})