from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import NUMBER_PAGINATE_BY, LOAN_STATUS_M, LOAN_STATUS_A, LOAN_STATUS_O, LOAN_STATUS_R
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.decorators import multiple_permissions_required


@multiple_permissions_required('catalog.can_mark_returned', 'catalog.can_edit')
def index(request):
    '''view func for home page of the app'''
    
    #define counts of some the main object
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    #Available book (status = 'a")
    num_instances_available = BookInstance.objects.filter(status__exact = LOAN_STATUS_A).count()

    #The all() is implied by default.
    num_author = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_author': num_author,
        'num_visits': num_visits,
    }
    
    #render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = NUMBER_PAGINATE_BY

    permission_required = ('catalog.can_mark_returned', 'catalog.change_book')

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'

    permission_required = ('catalog.can_mark_returned', 'catalog.change_book')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_instances'] = self.object.bookinstance_set.all()
        context['genres'] = self.object.genre.all()
        context['MAINTENANCE'] = LOAN_STATUS_M
        context['AVAILABLE'] = LOAN_STATUS_A
        return context
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = NUMBER_PAGINATE_BY

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact=LOAN_STATUS_O)
            .order_by('due_back')
        )
