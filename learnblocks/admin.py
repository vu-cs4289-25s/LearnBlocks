from django.contrib import admin
#from .models import LearnBlocks

class LearnBlocksAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')

# Register your models here.
#admin.site.register(LearnBlocks, LearnBlocksAdmin)