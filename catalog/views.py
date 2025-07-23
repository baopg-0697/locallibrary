import datetime
from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import NUMBER_PAGINATE_BY, LOAN_STATUS_M, LOAN_STATUS_A, LOAN_STATUS_O, LOAN_STATUS_R, INITIAL_DATE
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.decorators import multiple_permissions_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'
    paginate_by = NUMBER_PAGINATE_BY
    permission_required = 'catalog.view_author'
    
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
    
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

@permission_required('catalog.can_mark_returned')
def return_book_librarian(request, pk):
    """
    View để thủ thư đánh dấu một cuốn sách là đã được trả.
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Nếu người dùng xác nhận (gửi request POST)
    if request.method == 'POST':
        # Cập nhật trạng thái sách thành 'Available'
        book_instance.status = LOAN_STATUS_A
        book_instance.borrower = None # Xóa thông tin người mượn
        book_instance.save()
        # Chuyển hướng về trang danh sách sách đã mượn
        return HttpResponseRedirect(reverse('my-borrowed'))

    # Nếu là request GET, hiển thị trang xác nhận
    context = {
        'book_instance': book_instance,
    }
    
    return render(request, 'catalog/book_return_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = INITIAL_DATE
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    context_object_name = 'author'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )
