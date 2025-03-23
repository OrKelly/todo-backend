from django.contrib import admin

from .models import Category, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "deadline"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
