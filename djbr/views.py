from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect

from .models import Book, Author, Review

from django.urls import reverse

from django.utils import timezone

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

def index(request):
    latest_books_published = Book.objects.order_by('-pub_year', 'title')[:10]
    context = {'latest_books_published': latest_books_published}
    return render(request, 'djbr/index.html', context)

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'djbr/book.html', {'book': book})

def reviews(request, book_id):
    book = get_object_or_404(Book, pk=book_id)    
    book_reviews = book.review_set.all()
    context = {
        'book': book,
        'book_reviews': book_reviews
    }
    return render(request, 'djbr/reviews.html', context)

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'djbr/author.html', {'author': author})

@login_required(login_url='/djbr/login/')
def review(request, book_id, review_id=None):
    if review_id is not None:
        review = get_object_or_404(Review, pk=review_id)
    else:
        review = Review()
        review.book_id = book_id
    if request.method == 'POST':
        review.title = request.POST['title']
        review.text = request.POST['text']
        review.review_date = timezone.now()
        review.save()
        return HttpResponseRedirect(reverse('djbr:reviews', args=(book_id,)))
    else:
        context = {
        'book_id': book_id,
        'review_id': review_id,
        'title': review.title,
        'text': review.text
    }
    return render(request, 'djbr/review.html', context)

def profile(request, user_id=None):
    if request.method == 'POST':
        if request.POST['password'] != request.POST['confirm-password']:
            return render(request, 'djbr/profile.html', {
                'first_name': request.POST['first-name'],
                'last_name': request.POST['last-name'],
                'username': request.POST['username'],
                'email': request.POST['email'],
                'error_message': 'Passwords do not match',
                'error_code': 'password_mismatch'
            })
        if user_id is not None:
            user = User.objects.get(pk=user_id)
        else: 
            user = User.objects.create_user(request.POST['username'])        
        user.first_name = request.POST['first-name']
        user.last_name = request.POST['last-name']
        user.email = request.POST['email']
        user.set_password(request.POST['password'])
        user.save()
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
        return HttpResponseRedirect(reverse('djbr:index'))
    else:
        if user_id is not None and request.user.id == user_id:
            context = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'username': request.user.username,
                'email': request.user.email
            }
        else:
            context = {
                'first_name': '',
                'last_name': '',
                'username': '',
                'email': ''
            }
    return render(request, 'djbr/profile.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            dest = request.POST.get('next', reverse('djbr:index'))
            return HttpResponseRedirect(dest)
    return render(request, 'djbr/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('djbr:index'))    
    
