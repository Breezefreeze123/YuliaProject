from django.contrib import admin
from .models import Coffee, Category, TagTable

# Следующие методы регистрации аналогичны использованным декораторам @admin.register(Model):
# admin.site.register(Coffee, CoffeeAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(TagTable, TagTableAdmin)

admin.AdminSite.site_header='Yulia Administration'
admin.AdminSite.index_title='Coffeshop'

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    # fields = [("title",'slug'), "content",'cat']
    # exclude=['is_published']
    list_display=['id', 'title', 'is_published','cat', 'time_create']
    list_display_links=['id', 'title']
    ordering=['-time_create']
    list_editable=['cat']
    list_per_page=10
    actions=['set_published', 'set_draft']
    search_fields=['title', 'cat__title']
    search_help_text=['Поиск по наименованию продукта']
    list_filter=['cat__title', 'is_published']
    prepopulated_fields = {"slug": ["title"]}
    filter_horizontal=['tag']

    # Добавление действия для отметки опубликованными выбранных значений
    @admin.action(description="Mark selected as published")
    def set_published(self, request, queryset):
        queryset.update(is_published=True)

    # Добавление действия для снятия отметки опубликованными выбранных значений
    @admin.action(description="Mark selected as draft")
    def set_draft(self, request, queryset):
        queryset.update(is_published=False)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id', 'title']
    list_display_links=['id', 'title']
    ordering=['title']
    prepopulated_fields = {"slug": ["title"]}

@admin.register(TagTable)
class TagTableAdmin(admin.ModelAdmin):
    list_display=['id', 'tag']
    list_display_links=['id', 'tag']
    ordering=['tag']
    prepopulated_fields = {"slug": ["tag"]}