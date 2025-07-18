from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LOAN_STATUS

# Create your views here.
def index(request):
    '''view func for home page of the app'''
    
    #define counts of some the main object
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    #Available book (status = 'a")
    num_instances_available = BookInstance.objects.filter(status__exact = LOAN_STATUS).count()

    #The all() is implied by default.
    num_author = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_author': num_author,
    }
    
    #render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
