# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse

# from .forms import CommentForm, PostForm
from .models import Recipe, Ingredient


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'indexAuth.html', {
        'page': page,
        'paginator': paginator
    })