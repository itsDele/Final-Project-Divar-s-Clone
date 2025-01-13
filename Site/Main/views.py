from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import *
from .models import Ad, UserProfile, AdImage, ItemCategory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Home page showing ads
def MainPage(request):
    ads = Ad.objects.all()
    recs = get_recommendations(request, key='homepage_recs', as_dict=True)

    for ad in ads:
        ad.main_image = AdImage.objects.filter(ad=ad).first()  # Align with AdImage model

    context = {
        'homepage_recs': recs,
        'ads': ads,
    }

    return render(request, 'Market/ad_list.html', context)

def ad_detail_view(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    images = AdImage.objects.filter(ad=ad)

    recs = get_recommendations(request, key='ad_recs', as_dict=True)

    context = {
        'ad': ad,
        'ad_recs': recs,
        'images': images,
        'slug': ad.slug
    }
    return render(request, 'Market/ad_detail_view.html', context)

@login_required
def add_ad(request):
    if request.method == 'POST':
        ad_form = AdListingForm(request.POST)
        photo_form = AdImageForm(request.POST, request.FILES)

        if ad_form.is_valid():
            ad_instance = ad_form.save(commit=False)
            ad_instance.author = request.user
            ad_instance.save()

            files = request.FILES.getlist('photos')
            for file in files:
                AdImage.objects.create(ad=ad_instance, ad_image_file=file)

            return redirect('home')

    else:
        ad_form = AdListingForm()
        photo_form = AdImageForm()

    categories = ItemCategory.objects.exclude(parent__isnull=True)

    return render(request, 'Market/add_ad.html', {
        'ad_form': ad_form,
        'photo_form': photo_form,
        'categories': categories
    })

@login_required
def edit_ad(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    images = AdImage.objects.filter(ad=ad)

    if request.method == 'POST':
        form = AdListingForm(request.POST, request.FILES, instance=ad)

        if form.is_valid():
            try:
                ad = form.save()
                photo_files = request.FILES.getlist('photo_files')

                if photo_files:
                    AdImage.objects.filter(ad=ad).delete()
                    for file in photo_files:
                        AdImage.objects.create(ad=ad, ad_image_file=file)
                elif not images.exists():
                    raise ValueError("An ad requires at least one image.")
                
                messages.success(request, 'Ad updated!')
            except Exception as e:
                messages.error(request, f'Update failed: {str(e)}')
            return redirect('edit_ad', slug=ad.slug)
        else:
            messages.error(request, 'Update error.')

    else:
        form = AdListingForm(instance=ad)

    context = {
        'form': form,
        'ad': ad,
        'categories': ItemCategory.objects.all(),
        'images': images
    }

    return render(request, 'Market/edit_ad.html', context)

@login_required
def delete_ad(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if request.method == 'POST':
        try:
            ad.delete()
            messages.success(request, 'Ad deleted.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Deletion failed: {str(e)}')
            return redirect('edit_ad', slug=slug)
    return render(request, 'Market/delete_ad.html', {'ad': ad})

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(AdImage, id=photo_id)
    ad = photo.ad  # Ensure this relates correctly

    if request.method == 'POST':
        try:
            if ad.images.count() > 1:  # Ensure at least one image remains
                photo.delete()
                return JsonResponse({'success': True})
            else:
                raise ValueError('Must keep one image.')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method.'}, status=400)

# User registration and login
def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            signup_form = RegistrationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, 'Registered successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Registration issue.')
        else:
            signup_form = RegistrationForm()
        return render(request, 'User/signup.html', {'signup_form': signup_form})
    else:
        return redirect('home')

def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            login_form = SignInForm(request=request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["user_name"]
                password = login_form.cleaned_data["user_password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid credentials.')
            else:
                messages.error(request, 'Invalid credentials.')
        else:
            login_form = SignInForm()
        return render(request, 'User/login.html', {'login_form': login_form})
    else:
        return redirect('home')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/login/")

# Get advertisement suggestions
def suggest_ads_template(request):
    if request.is_ajax() and request.method == 'GET':
        query = request.GET.get('query', '')
        ads = Ad.objects.filter(title__icontains=query)  # Adjust filtering as needed
        suggestions = [{"title": ad.title, "slug": ad.slug} for ad in ads]
        return JsonResponse(suggestions, safe=False)

    return JsonResponse({"error": "Invalid request"}, status=400)

def get_recommendations(request, key='recs', as_dict=False):
    query = request.GET.get('search', '')
    cat = request.GET.get('category', '')

    if query:
        ads = Ad.objects.filter(title__icontains=query)
        context = {key: ads}
        return render(request, 'ad_list_display.html', context)

    if not cat:
        if as_dict:
            return []
        return render(request, 'no_results_found.html')

    try:
        category = ItemCategory.objects.get(name__iexact=cat)  # Check category name
    except ItemCategory.DoesNotExist:
        if as_dict:
            return []
        return render(request, 'no_results_found.html')

    ads = Ad.objects.filter(category=category)

    ad_data = [f"{ad.title} {ad.description}" for ad in ads]
    ad_data.append(cat)
    context = {key: ad_data}
    return render(request, 'ad_list_display.html', context)

# Error handlers
def error_403(request, exception=None):
    return render(request, 'errors/error_403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/error_404.html', status=404)

def error_500(request):
    return render(request, 'errors/error_500.html', status=500)