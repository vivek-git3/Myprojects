from django.contrib import admin
from .models import Category, Tip

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Fields to display in the list view
    search_fields = ('name',)  # Add search functionality

# Register the Tip model (if not already registered)
@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'category')  # Fields to display
    search_fields = ('title', 'content')  # Add search functionality
    list_filter = ('category',)  # Filter tips by category
