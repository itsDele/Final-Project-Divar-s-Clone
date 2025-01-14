from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Advertising, User, Note, AdvertisingImage, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def HomePage(request):
    advertisements = Advertising.objects.all()
    for advertisement in advertisements:
        advertisement.first_image = AdvertisingImage.objects.filter(advertising=advertisement).first()
    
    context = {
        'advertisements': advertisements,
    }
    return render(request, 'Market/product_list.html', context)

def product_detail(request, slug):
    advertisement = get_object_or_404(Advertising, slug=slug)
    image = AdvertisingImage.objects.filter(advertising=advertisement)

    context = {
        'advertisement': advertisement,
        'image': image,
    }
    return render(request, 'Market/product_detail.html', context)

@login_required
def create_advertising(request):
    if request.method == 'POST':
        advertisement_form = AdvertisingForm(request.POST)
        image_form = AdvertisingImageForm(request.POST, request.FILES)

        if advertisement_form.is_valid():
            advertisement = advertisement_form.save(commit=False)
            advertisement.owner = request.user
            advertisement.save()
            images = request.FILES.getlist('image')
            for image in images:
                AdvertisingImage.objects.create(advertising=advertisement, image=image)

            return redirect('home')
    else:
        advertisement_form = AdvertisingForm()
        image_form = AdvertisingImageForm()

    categories = Category.objects.exclude(parent__isnull=True)

    return render(request, 'Market/create_ad.html', {
        'advertisement_form': advertisement_form,
        'image_form': image_form,
        'categories': categories
    })

@login_required
def edit_ad(request, slug):
    advertisement = get_object_or_404(Advertising, slug=slug)
    if request.method == 'POST':
        advertisement_form = AdvertisingForm(request.POST, instance=advertisement)
        if advertisement_form.is_valid():
            advertisement_form.save()
            messages.success(request, 'Advertisement updated successfully.')
            return redirect('product_detail', slug=advertisement.slug)
    else:
        advertisement_form = AdvertisingForm(instance=advertisement)

    return render(request, 'Market/edit_ad.html', {
        'advertisement_form': advertisement_form,
        'advertisement': advertisement,
    })

# Your existing user_signup etc...