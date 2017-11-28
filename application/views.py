from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Q
idOwner, nameOwner, startLetter = 0, "", "A"

from application.models import Movie,Rating,Settings, RatingForm

import random    
import factor_matrix
import json
from django.http import JsonResponse

def getOrCreateUserCookie(session):
    #return 2

    if 'user_id' not in session:
        current_id = Settings.objects.get(name='numUsers')
        newID = int(current_id.value)
        session['user_id'] = newID 
        current_id = str( newID+1 )
        current_id.save()
    
    return session['user_id']

def IndexView(request):
    TEMPLATE = 'application/Main.html'
    RESULT_TEMPLATE = 'application/results.html'
    user_id = getOrCreateUserCookie(request.session)
    
    #TODO: ignore films user has already rated
    movies = list(Movie.objects.values())
    random.shuffle(movies) # shuffle in-place

    def post(self, request):
        return HttpResponse(json.dumps({'key': 'value'}), mimetype="application/json")

    # if request.method == "POST":
    #     user_rating = Rating()
    #     user_rating.user = request.POST['user_id']
    #     user_rating.movie = Movie.objects.get( id=item[1] ) 
    #     user_rating.rating = request.POST['rating']
    #     user_rating.save()
        
    return render(request, TEMPLATE, {
      'object_list' : movies[:5]
    })

def ResultsView(request):

    TEMPLATE = 'application/results.html'
    user_id = getOrCreateUserCookie(request.session)

    # #TODO: if the user doesn't have any recommended movies yet just provide some defaults
    recommendedMovies = factor_matrix.getGuessedRatings(user_id)[:5]

    return render(request, TEMPLATE, {
         'object_list' : recommendedMovies
    })

    #response = JsonResponse({'object_list' : recommendedMovies})
    #return response
   
#class ResultsView(generic.ListView):
#    template_name = 'application/results.html'

#    def get_queryset(self):
#        """Do Nothing"""

#-----------------------------------------------------#
class RatingsView(generic.ListView):
    template_name = 'application/Rating2.html'

    def get_queryset(self):
        """Do Nothing"""

def recommend(request):
    global idOwner, nameOwner, startLetter
    slCopy = startLetter
    idOwner = getOrCreateUserCookie(request.session)
    if idOwner == 0: #Attempt to hit this page directly - don't allow; redirect to home
        nameOwner = ""
        return HttpResponseRedirect("")
    if request.method == "POST":
        for key in request.POST.keys():
            if key not in ["rmovie", "csrfmiddlewaretoken", "mr"]: # 3 parameters that POST sends, check for additional
                startLetter = key
        rmovie = request.POST.get("rmovie", "")
        mrating = request.POST.get("mr", "")
        if startLetter == "Rate" and rmovie != "": #user pressed "RATE" button
            getMovie=Movie.objects.filter(title=rmovie)
            if getMovie.exists():
                tryRating, created = Rating.objects.get_or_create(user = idOwner, id = Movie.id,
                  defaults={'rating': mrating})
                if not created:
                    newRating = Rating(idrating = tryRating.idrating, user = idOwner, id = Movie.id, rating = mrating)
                    newRating.save()
            else:
                newMovie = Movie(title=rmovie)
                newMovie.save()
                newM=Movie.objects.filter(title=rmovie)
                newRating = Rating(user = idOwner, id = newM[0].id, rating = mrating)
                newRating.save()
    if startLetter == "Rate":
        startLetter= slCopy
    getMovies = Movie.objects.filter(Q(title__startswith=startLetter) | Q(title__startswith=startLetter.lower())).order_by('rating')[:10]
    return render(request, "application/Rating2.html", {"note": "", "response": getMovies, "startLetter": startLetter, "user": idOwner})
