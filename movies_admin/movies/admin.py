from django.contrib import admin
from .models import Genre, Filmwork, Genre_Filmwork, Person, Person_Filmwork

#стили
class Genre_Filmwork_Inline(admin.TabularInline):
    model = Genre_Filmwork
    extra = 1 
    
class Person_Filmwork_Inline(admin.TabularInline):
    model = Person_Filmwork
    autocomplete_fields = ['person']
    extra = 1


#Модели
@admin.register(Genre)
class Genre_Admin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created']


@admin.register(Filmwork)
class Filmwork_Admin(admin.ModelAdmin):
    inlines = [Genre_Filmwork_Inline, Person_Filmwork_Inline]
    list_display = ['title', 'type', 'created', 'rating']
    list_filter = ['type']
    search_fields = ['title']
    

@admin.register(Person)
class Person_admin(admin.ModelAdmin):
    list_display = ['full_name', 'created']
    search_fields = ['full_name']


# @admin.register(Genre_Filmwork)
# class Genre_Filmwork_m2m_Admin(admin.ModelAdmin):
#     raw_id_fields = ["film_work", "genre"]  


# @admin.register(Person_Filmwork)
# class Person_Filmwork_m2m_admin(admin.ModelAdmin):
#     pass  