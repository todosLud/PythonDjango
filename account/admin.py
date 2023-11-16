from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Carousel, CategoriaCarousel, UserProfile
# Register your models here.

@admin.register(CategoriaCarousel)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']
    

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'sottotitolo', 'categoria', 'img_preview', 'pubblicato']
    search_fields = ['titolo', 'sottotitolo', 'categoria', 'corpo']
    list_filter = ['titolo', 'sottotitolo','categoria','pubblicato']
    readonly_fields = ['img_preview']
    list_editable = ['pubblicato']


class CustomUserAdmin(admin.StackedInline):
    model = UserProfile
    can_delete = False
    readonly_fields = ['img_preview']
    
#creo la nuova view del account user in admin
class AccountsUserAdmin(UserAdmin):
    
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(AccountsUserAdmin, self).add_view(*args, **kwargs)
    
    def change_view(self, *args, **kwargs):
        self.inlines = [CustomUserAdmin]
        return super(AccountsUserAdmin, self).change_view(*args, **kwargs)
    
admin.site.unregister(User)    
admin.site.register(User, AccountsUserAdmin)
