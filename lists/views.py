from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item
# Create your views here.


def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items_list = Item.objects.all()
    return render(request, 'lists.html',
                  {'items': items_list})

def new_list(request):
    Item.objects.create(
        text=request.POST['item_text'])
    return redirect('/lists/newly-list/')
