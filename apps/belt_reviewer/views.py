from django.shortcuts import render, redirect
def index( request ):
    return render( request, "belt_reviewer/index.html" )

# Create your views here.
