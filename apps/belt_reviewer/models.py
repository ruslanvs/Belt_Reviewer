from __future__ import unicode_literals
print "*"*25 + " MODELS.PY " + "*"*25

from django.db import models
import re, bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager( models.Manager ):
    def signup_validation( self, post_data ):
        errors = {}
        nlen_min = 2
        pwlen_min = 8

        # FORM INPUT VALIDATIONS
        # VALIDATE FIRST NAME
        if len( post_data['fname'] ) < nlen_min: # NAME LENGTH
            errors["fname"] = "First name cannot be less than " + str( nlen_min ) + " characters. "

        elif not str.isalpha( str( post_data['fname'] ) ): # NAME CONVENTIONS
            errors["fname"] = "Invalid characters in the first name. "
    
        # VALIDATE LAST NAME
        if len( post_data['lname'] ) < nlen_min: # NAME LENGTH
            errors["lname"] = "Last name cannot be less than " + str( nlen_min ) + " characters. "

        elif not str.isalpha( str( post_data['lname'] ) ): # NAME CONVENTIONS
            errors["lname"] = "Invalid characters in the last name. "

        # VALIDATE EMAIL
        if not email_regex.match( post_data['email'] ): # EMAIL CONVENTIONS
            errors["email"] = post_data['email'] + "is not a valid email. "

        else: # CHECK IF EMAIL IS ALREADY IN USE
            existing_user = User.objects.filter( email = post_data['email'] ).first()
            if existing_user:
                errors["email"] = "Email " + post_data['email'] + " is already in use"

        # VALIDATE PASSWORD CONVENTIONS AND REPEAT
        if len( str( post_data['pw'] ) ) < pwlen_min:
            errors["pw"] = "Password should have at least " + str( pwlen_min ) + " characters"
        elif post_data['pw'] != post_data['pwc']:
            errors["pw"] = "Password confirmation does not match"

        if errors:
            print "*"*25, "SIGNUP ERRORS: ", errors, "FORM DATA: ", post_data
            return errors
        else: # SUCCESS - ADD NEW USER INTO THE DATABASE
            print "*"*25, "VALIDATION SUCCESSFUL. FORM DATA: ", post_data
            User.objects.create(
                fname = post_data['fname'],
                lname = post_data['lname'],
                email = post_data['email'],
                pw = bcrypt.hashpw( post_data['pw'].encode(), bcrypt.gensalt() )
            )
            # >> not returning anything here explicitly?

    def login_validation( self, post_data ):
        # EMAIL VALIDATION
        errors = {}
        if not email_regex.match( post_data['email'] ): # EMAIL CONVENTIONS
            errors["email"] = post_data['email'] + "is not a valid email. "
        else:
            existing_user = User.objects.filter( email = post_data['email'] ).first()
            if not existing_user:
                errors["email"] = "Email " + post_data['email'] + " is not registered with any user"
            else: # CHECK PW
                # if User.objects.get( email = post_data['email'] ).pw != post_data['pw']:
                if not bcrypt.checkpw( post_data['pw'].encode(), User.objects.get( email = post_data['email'] ).pw.encode() ):
                    errors["pw"] = "Wrong password"
        # print "*"*25, "LOGIN ERRORS:", errors
        return errors

class AuthorManager( models.Manager):
    def validator( self, post_data ):
        errors = {}
        
        # VALIDATE AUTHOR NAME
        if not post_data['author'] and not post_data['new_author']:
            errors["author"] = "Please select an author from the list or add a new author."
            if post_data['author'] and post_data['new_author']: # CHECKING FOR DUPLICATE INPUT
                errors["author"] = "Please select either an author from the list or add a new author, not both."
            elif post_data['new_author']: #FURTHER, VALIDATING NEW AUTHOR ONLY
                nlen_min = 2
                if len( post_data['new_author'] ) < nlen_min:
                    errors["new_author"] = "Author name cannot be less than " + str( nlen_min ) + " characters. "
                else: 
                    existing_author = Author.objects.filter( name = post_data['new_author'] ).first()
                    if existing_author: # UNIQUESNESS CHECK
                        errors["new_author"] = "Author " + post_data['new_author'] + " already exists. If you mean to pick " + post_data['new_author'] + ", please select this author from the drop-down list above."

        if errors:
            return errors

    def create( self, post_data ):
        if post_data['new_author']:
            Author.objects.create(
                name = post_data['new_author']
            )
            author = Author.objects.get( name = post_data['new_author'] ) #>> check if this is available in other classes
        else:
            author = Author.objects.get( id = post_data['author'] )
        print '*'*25, "MODELS.PY AUTHOR:", author
        return author

class BookManager( models.Manager ):
    def validator( self, post_data, user_id ): #>> check if user id is needed here
        errors = {}
        
        # VALIDATE NEW BOOK TITLE
        tlen_min = 2
        if len( post_data['title'] ) < tlen_min:
            errors["title"] = "Title cannot be less than " + str( tlen_min ) + " characters. "
        else:
            existing_title = Book.objects.filter( title = post_data['title'] ).first()
            if existing_title:
                errors["title"] = "Title " + post_data['title'] + " already exists."

        if errors:
            return errors

    def create( self, post_data, user_id, author ):
        Book.objects.create(
            title = post_data['title'],
            author = author, #>> check if this is available from Author class
            user = User.objects.get( id = user_id )
        )

class ReviewManager( models.Manager ):
    def validator( self, post_data, user_id ): #>> check if user id is needed here
        print '*'*25, 'REVIEW MANAGER POST DATA:', post_data
        errors = {}

        # VALIDATE REVIEW CONTENT
        clen_min = 10
        if len( post_data['content'] ) < clen_min:
            errors["content"] = "The review cannot be less than " + str( clen_min ) + " characters. "

        if errors:
            return errors

    def create( self, post_data, user_id ):
        Review.objects.create(
            content = post_data['content'],
            rating = post_data['rating'],
            user = User.objects.get( id = user_id ),
            book = Book.objects.get( title = post_data['title'] )
        )

class User( models.Model ):
    fname = models.CharField( max_length = 255 )
    lname = models.CharField( max_length = 255 )
    email = models.CharField( max_length = 255 )
    pw = models.CharField( max_length = 255 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = UserManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", name: " + self.fname + " " + self.lname

class Author( models.Model ):
    # user = models.OneToOneField( User, related_name="author" )
    name =  models.CharField( max_length = 255, blank = True  )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = AuthorManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", name: " + str( self.name )

class Book( models.Model ):
    user = models.ForeignKey( User, related_name = "books" )
    author = models.ForeignKey( Author, related_name = "books")
    title = models.CharField( max_length = 255 )
    desc = models.TextField( max_length = 1000, blank = True ) #>> non used
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = BookManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", title: " + self.title

class Review( models.Model ):
    user = models.ForeignKey( User, related_name="reviews" )
    book = models.ForeignKey( Book, related_name="reviews" )
    liked_users = models.ManyToManyField( User, related_name="liked_reviews" )
    content = models.TextField( max_length = 1000, blank = True )
    rating = models.IntegerField()
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = ReviewManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", rating: " + str( self.rating ) + ", content: " + self.content

# QUERIES
# Book.objects.create( title = "Way to health", desc = "Healthy foods and living", author_id = 1)
# Review.objects.create( content = "Very helpful book", rating = 5, user_id = 3, book_id = 1 )
# Review.objects.get(id = 2).delete()
# User.objects.all()
# Author.objects.all()
# Book.objects.all()
# Review.objects.all()
# Author.objects.values_list('user__fname')