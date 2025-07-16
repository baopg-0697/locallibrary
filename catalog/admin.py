from django.contrib import admin
from .models import Genre, Author, Book, BookInstance
# Register your models here.
admin.site.register(Genre)

#Register the author admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

#Class bookinstance inline class book
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Register the Admin classes for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

    def display_genre(self, obj):
        """Crequired to display genre in Admin."""
        return ', '.join(genre.name for genre in obj.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

# Register the Admin classes for BookInstance
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
