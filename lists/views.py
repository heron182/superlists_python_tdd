from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError


def home_page(request):
    return render(request, 'home.html',
                  {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'lists.html',
                  {'list': list_,
                   'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        new_list = List.objects.create()
        form.save(for_list=new_list)
        return redirect(new_list)
    else:
        return render(request, 'home.html', {'form': form})
