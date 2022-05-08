from core.models import User
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    search_fields = ('name', )
    list_filter = ('is_active', )
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active',
    )

