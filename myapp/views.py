from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_safe
from .models import Book
from .forms import BookForm

@require_safe
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@require_safe
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

@require_http_methods(["GET", "POST"])
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

@require_http_methods(["GET", "POST"])
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form, 'book': book})

@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})
