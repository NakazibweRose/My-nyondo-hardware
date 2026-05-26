from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('username','is_active','is_staff','is_superuser',
    )

    list_filter = ('is_active','is_staff',
    )

    search_fields = ('username',
    )