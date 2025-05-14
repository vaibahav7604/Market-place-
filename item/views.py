from django.shortcuts import render, get_object_or_404,redirect
from .models import Item, Category
from item.forms import ItemForm, EditItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


def non(request):
    query=request.GET.get('query','')
    categories=Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if query:
        items=items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request,'item/browes.html',{
        'items':items,
        'query':query
    })


def detail(request,pk):
    item=get_object_or_404(Item,pk=pk)
    related_items=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[:4]

    return render(request,'item/detail.html',{
        'item':item,
        'related_items':related_items
    })
@login_required
def new(request):
    if request.method == 'POST':
        form = ItemForm(request.POST,request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail',pk=item.id)

    else:
        form = ItemForm()
    return render(request,'item/item.html',{
        'form':form
    })
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:dashboard')

@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST,request.FILES,instance=item)

        if form.is_valid():
            item.save()
            return redirect('item:detail',pk=item.id)

    else:
        form = EditItemForm(instance=item)
    return render(request,'item/item.html',{
        'form':form
    })