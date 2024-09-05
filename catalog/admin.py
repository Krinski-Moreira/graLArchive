from django.contrib import admin

# Register your models here.
from .models import Lens, LensComponent

#admin.site.register(Lens)
#admin.site.register(LensComponent)
# Register the Admin classes for LEns using the decorator
@admin.register(Lens)
class LensAdmin(admin.ModelAdmin):
    list_display = ("Name", "Author", "GraL", "Max_separation")

# Register the Admin classes for LensComponent using the decorator
@admin.register(LensComponent)
class LensComponentAdmin(admin.ModelAdmin):
    list_display = ("Name", "Component", "RA_best", "DEC_best")