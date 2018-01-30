print "*"*25, "VIEWS.PY", "*"*25

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book, Review, Author

def index( request ):
    if not request.session['logged_in_user_id']:
        return render( request, "belt_reviewer/index.html" )
    else:
        return redirect( "/belt_reviewer/books" )

def logout( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        request.session['logged_in_user_id'] = False
        return redirect( "/belt_reviewer" )

def login( request ):
    print "*"*25, "VIEWS.PY LOGIN ROUTE", "*"*25
    print "*"*25, "NEXT: ", request.POST['from']
    print "*"*25, "REQUEST PATH: ", request.path
    print "*"*25, "HTTP REFER: ", request.META.get('HTTP_REFERER')
    if not request.session['logged_in_user_id']:#IF LOGGED IN ALREADY, THEN GOES TO BOOKS
        errors = User.objects.login_validation( request.POST )
        if errors:
            messages.error( request, errors )
            return redirect( "/belt_reviewer" ) #>> check if this is a good way to refer to the route
        else:
            request.session['logged_in_user_id'] = User.objects.get( email = request.POST['email'] ).id # >> check with Shane how to establish the session at the Models.py level. When I tried it, it could not recognize the "request" variable.
            return redirect( "/belt_reviewer/books" )
    else:
        return redirect( "/belt_reviewer/books" )

def signup( request ):
    if not request.session['logged_in_user_id']: #IF LOGGED IN ALREADY, THEN GOES TO BOOKS
        errors = User.objects.signup_validation( request.POST ) #>> lay out messages around the index page
        if errors:
            messages.error( request, errors )
            return redirect( "/belt_reviewer" ) #>> check if this is a good way to refer to the route
        else:
            request.session['logged_in_user_id'] = User.objects.get( email = request.POST['email'] ).id # >> check with Shane how to establish the session at the Models.py level. When I tried it, it could not recognize the "request" variable.
            messages.success( request, "Your user data has been saved" )
            return redirect( "/belt_reviewer/books" )
    else:
        return redirect( "/belt_reviewer/books" )

def books( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        request.session['fname'] = User.objects.get( id = request.session['logged_in_user_id'] ).fname
        request.session['lname'] = User.objects.get( id = request.session['logged_in_user_id'] ).lname
        page_data = {
            "latest_reviews": Review.objects.order_by('-created_at')[:3],
            "other_reviews": Review.objects.order_by('-created_at')[3:]
        }
        return render ( request, "belt_reviewer/books.html", page_data )

def books_all( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        page_data = {
            "books": Book.objects.all()
        }
        return render ( request, "belt_reviewer/books_all.html", page_data )

def book_show( request, id ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        page_data = {
            "id": id,
            "book": Book.objects.get( id = id ),
            "reviews": Review.objects.order_by('-created_at').filter( book_id = id )
        }
        return render( request, "belt_reviewer/book_show.html", page_data )

def books_and_reviews_new( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        page_data = {
            'authors': Author.objects.all()
        }
        return render( request, "belt_reviewer/books_and_reviews_new.html", page_data )

def books_and_reviews_create( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:

        errors = Author.objects.validator( request.POST )
        if errors:
            messages.error( request, errors )
            return redirect( "/belt_reviewer/books_and_reviews/new" )

        errors = Book.objects.validator( request.POST, request.session['logged_in_user_id'] )
        if errors:
            messages.error( request, errors )
            return redirect( "/belt_reviewer/books_and_reviews/new" )

        errors = Review.objects.validator( request.POST, request.session['logged_in_user_id'] )
        if errors:
            messages.error( request, errors )
            return redirect( "/belt_reviewer/books_and_reviews/new" )

        print '*'*25, "REQUEST.POST:", request.POST
        author = Author.objects.create( request.POST )
        print '*'*25, "VIEWS.PY AUTHOR:", author

        Book.objects.create( request.POST, request.session['logged_in_user_id'], author )
        Review.objects.create( request.POST, request.session['logged_in_user_id'] )

        messages.success( request, "Your book and review have been saved" )
        id = Book.objects.get( title = request.POST['title'] ).id
        return redirect( "/belt_reviewer/books" ) #>>> chech

def review_create( request, id ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        errors = Review.objects.validator( request.POST, request.session['logged_in_user_id'] )
        if errors:
            messages.error( request, errors )
            return redirect( "/belt_reviewer/books_and_reviews/new" )
        else:
            Review.objects.create( request.POST, request.session['logged_in_user_id'] )
            messages.success( request, "Review has been saved" )
            id = id
            return redirect( "/belt_reviewer/books/" + id + "/show" ) #>>> plugged for now

def user_show( request, id ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        page_data = {
            "user": User.objects.get( id = id ),
            "reviews": Review.objects.filter( user_id = id ),
            "reviews_total": Review.objects.filter( user_id = id ).count()
        }
        return render( request, "belt_reviewer/user_show.html", page_data )

def review_destroy( request, id ):
    if not request.session['logged_in_user_id']:
        return redirect( "/belt_reviewer" )
    else:
        Review.objects.get( id = id ).delete()
        messages.success( request, "Your review has been deleted")
        return redirect( "/belt_reviewer/books" )

        
# Create your views here.
