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
    error = None
    if request.method == 'POST':
        new_item = Item(list=list_,
                        text=request.POST['item_text'])
        try:
            new_item.full_clean()
            new_item.save()
        except ValidationError:
            error = 'You can\'t add an empty item'
        else:
            return redirect(list_)
    return render(request, 'lists.html',
                  {'list': list_,
                   'error': error})


def new_list(request):
    new_list = List.objects.create()
    new_item = Item(
        text=request.POST['item_text'],
        list=new_list)
    try:
        new_item.full_clean()
        new_item.save()
    except ValidationError:
        new_list.delete()
        error = 'You can\'t add an empty item'
        return render(request, 'home.html', {'error': error})
    return redirect(new_list)
