#use include() to add paths from the catalog application
from django.urls import include
from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # URL cho người dùng đã đăng nhập
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    
    # URL cho nhân viên thư viện
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:pk>/return/', views.return_book_librarian, name='url-to-return-book-view'),
    
    # URL cho Author Create, Update, Delete
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
] 
