from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import NUMBER_PAGINATE_BY, LOAN_STATUS_M, LOAN_STATUS_A, LOAN_STATUS_O, LOAN_STATUS_R
from django.views import generic
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    '''view func for home page of the app'''
    
    #define counts of some the main object
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    #Available book (status = 'a")
    num_instances_available = BookInstance.objects.filter(status__exact = LOAN_STATUS_A).count()

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

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'catalog/book_list.html'
    paginate_by = NUMBER_PAGINATE_BY


class BookDetailView(generic.DetailView):
    model = Book
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_instances'] = self.object.bookinstance_set.all()
        context['genres'] = self.object.genre.all()
        context['MAINTENANCE'] = LOAN_STATUS_M
        context['AVAILABLE'] = LOAN_STATUS_A
        return context
