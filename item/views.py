from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category, Conversation,Message
from item.forms import ItemForm, EditItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

def non(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'item/browes.html', {
        'items': items,
        'query': query
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:4]
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'item/item.html', {
        'form': form
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:dashboard')

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.pk)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/item.html', {
        'form': form
    })

@login_required
def new_conversation(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user == item.created_by:
        messages.error(request, "You cannot contact yourself.")
        return redirect('item:detail', pk=pk)
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if not message_content:
            messages.error(request, "Message cannot be empty.")
            return render(request, 'item/contact_seller.html', {'item': item})
        conversation, created = Conversation.objects.get_or_create(
            item=item,
            buyer=request.user
        )
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=message_content
        )
        messages.success(request, "Conversation started! Check your inbox.")
        return redirect('item:inbox')
    return render(request, 'item/contact_seller.html', {'item': item})

@login_required
def conversation_chat(request, pk):
    try:
        conversation = get_object_or_404(Conversation, pk=pk)
        if request.user != conversation.buyer and request.user != conversation.item.created_by:
            messages.error(request, "You don't have access to this conversation.")
            return redirect('item:detail', pk=conversation.item.pk)
        if request.method == 'POST':
            message_content = request.POST.get('message')
            if message_content:
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    content=message_content
                )
                messages.success(request, "Message sent!")
            else:
                messages.error(request, "Message cannot be empty.")
            return redirect('item:conversation', pk=conversation.pk)
        return render(request, 'item/conversation.html', {
            'conversation': conversation,
            'item': conversation.item
        })
    except Exception as e:
        messages.error(request, "This conversation does not exist or was deleted.")
        return redirect('item:inbox')

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(item__created_by=request.user)
    ).distinct().order_by('-created_at')
    return render(request, 'item/inbox.html', {'conversations': conversations})