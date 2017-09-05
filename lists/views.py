from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'lists.html',
                  {'list': list_})


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
    return redirect('/lists/%s/' % new_list.id)


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],
                        list=list_)
    return redirect('/lists/%s/' % list_.id)
