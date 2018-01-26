from __future__ import unicode_literals
from django.db import models

class User( models.Model ):
    fname = models.CharField( max_length = 255 )
    lname = models.CharField( max_length = 255 )
    email = models.CharField( max_length = 255 )
    pw = models.CharField( max_length = 255 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", name: " + self.fname + " " + self.lname

class Author( models.Model ):
    user = models.OneToOneField( User, primary_key = True )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    def __unicode__( self ):
        return "id: " + str( self.id )

class Book( models.Model ):
    users = models.ManyToManyField( User, related_name = "books" )
    author = models.ForeignKey( Author, related_name = "books")
    title = models.CharField( max_length = 255 )
    decs = models.TextField( max_length = 1000, blank = True )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", title: " + self.title

class Review( models.Model ):
    user = models.ForeignKey( User, related_name="reviews" )
    content = models.TextField( max_length = 1000, blank = True )
    rating = models.IntegerField()
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", rating: " + self.title + ", content: " + self.content