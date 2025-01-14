from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Ad, ItemCategory, Location, AdImage
from .forms import MyUserCreationForm, MyUserUpdateForm

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'is_staff',
        'slug_identifier'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'slug_identifier')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_registered',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'phone',
                'password1',
                'password2',
                'slug_identifier'
            ),
        }),
    )
    ordering = ('username',)
    filter_horizontal = ()
    list_filter = ()
    form = MyUserUpdateForm
    add_form = MyUserCreationForm

class AdvertisementImageInline(admin.TabularInline):
    model = AdImage
    extra = 1

@admin.register(Ad)
class CustomAdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "city_location",
        "ad_category",
        "created_on",
        "updated_on",
    )
    list_filter = (
        "city_location",
        "ad_category",
        "created_on",
    )
    search_fields = ("title", "description",)
    ordering = ("-created_on",)
    prepopulated_fields = {'slug_identifier': ('title',)}
    inlines = [AdvertisementImageInline]

@admin.register(Location)
class CustomCityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ItemCategory)
class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    list_filter = ('parent_category',)
    search_fields = ('name',)