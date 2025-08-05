from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Book
from .forms import BookForm


@login_required
def book_list(request):
    books = Book.objects.all()  # Get all Book records from the database
    return render(request, 'books/book_list.html', {'books': books})

def book_create_NODEBUG(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request,'books/book_form.html',{'form':form, 'action':'Create'})



def book_create(request):
    form = BookForm(request.POST or None)

    if request.method == 'POST':
        print("POST received!")  # 🔍 Confirm POST hit
        print("POST data:", request.POST)  # 🔍 Show data sent

        if form.is_valid():
            form.save()
            print("Form saved!")  # ✅ Did this print?
            return redirect('book_list')
        else:
            print("Form errors:", form.errors)  # 🔍 See why it failed
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Create'})

def book_update(request):
    return render('books/error.hml')

def book_delete(request):
    return render('books/error.hml')


def book_overviews(request):
    return render(request, 'books/book_overviews.html')
    
    
def book_profile(request):
    return render(request, 'books/book_profile.html')