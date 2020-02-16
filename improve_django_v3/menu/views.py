from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Menu, Item
from .forms import MenuForm

def menu_list(request):

    '''Select all menus that have an expiration date
    greater than or equal today. Sort them by'''
    user = request.user
    menus = Menu.objects.filter(
        expiration_date__gt=timezone.now()
    ).prefetch_related("items")
    # menus = Menu.objects.all().filter(prefetch_related("items")
    # menus = []
    # for menu in all_menus:
    #     if menu.expiration_date >= timezone.now():
    #         menus.append(menu) # database hit

    # menus = sorted(menus, key=attrgetter('expiration_date'))
    return render(
        request, 'menu/list_all_current_menus.html', {'menus': menus}
    )

def menu_detail(request, pk):
    '''Display a menu that is passed a valid pk or 404'''
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


@login_required
def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save() # new menu created
            form.save_m2m()
            messages.info(
                request, f"Menu added: {form.cleaned_data['season']}"
            )
            return redirect(
                reverse('menu:menu_detail', kwargs={'pk': menu.pk})
            ) # display the new menu
    else:
        form = MenuForm() # provide a form to create a new menu 
    return render(request, 'menu/menu_edit.html', {'form': form})


@login_required
def edit_menu(request, pk):
    current_menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=current_menu)
        if form.is_valid():
            form.save()
            messages.info(
                request,
                'Menu is up to date!'
            )
            return HttpResponseRedirect(
                reverse("menu:menu_detail", kwargs={'pk': pk})
            )
    else:
        form = MenuForm(instance=current_menu)
    return render(request, 'menu/change_menu.html', {
            'form': form,
            'menu': current_menu
        })
    # items = Item.objects.all()
    # if request.method == "POST":
    #     menu.season = request.POST.get('season', '')
    #     menu.expiration_date = datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y')
    #     menu.items = request.POST.get('items', '')
    #     menu.save()

    # return render(request, 'menu/change_menu.html', {
    #     'menu': menu,
    #     'items': items,
    #     })

