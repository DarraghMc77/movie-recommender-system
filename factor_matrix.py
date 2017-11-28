from application.models import Movie, Rating, Settings
from django.db.models import Max, Count
import numpy as np
import os
import threading
import time

def factor_matrix_impl(R,K):
    optimumDifference = 0.1
    iterations = 20
    lambda_ = 0.0002

    (u, i) = R.shape

    p = 5*np.random.rand(u,K)
    q = 5*np.random.rand(K,i)

    W = R>0.5
    W[W == True] = 1
    W[W == False] = 0
    W = W.astype(np.float64, copy=False)

    # q <- (pT * p)^-1 * pT * r
    # p <- r*q*(qT* q)^-1
    lambda_ = 0.0002 * np.eye(K)
    for ii in xrange(iterations):
        print(ii)

        for u, Wu in enumerate(W):
            d = np.diag(Wu)

            t1 = np.dot(q, np.dot(d, q.T)) + lambda_
            t2 = np.dot(q, np.dot(d, R[u].T))

            p[u] = np.linalg.solve(t1,t2).T

        for i, Wi in enumerate(W.T):
            d = np.diag(Wi)

            t1 = np.dot(p.T, np.dot(d,p)) + lambda_
            t2 = np.dot(p.T, np.dot(d, R[:,i]))
            
            q[:,i] = np.linalg.solve(t1, t2) 

    return roundMatrix(np.dot(p,q))

def calcError(R,V,U,K,B):
    #checks the overall error between the provided ratings and predicted ratings
    error=0
    for row in xrange(len(R)):
            for column in xrange(len(R[row])):
                if R[row][column] > 0:
                    error =error + pow(R[row][column] - np.dot(U[row,:],V[:,column]),2)
                    for features in xrange(K):
                        error = error + (B/2) * (pow(U[row][features],2) + pow(V[features][column],2))
    return error;

def roundMatrix(nR):
    # rounds of the float ratings in the matrix and limits the maximum rating to 5 since
    # there's cases where the ratings can be greater than 5 due to the randomisation of U and V
    return np.minimum(np.round(nR), 5)
    
def getGuessedRatings(u):
    ids = Rating.objects.filter(user = u, isGuessed=True)\
                      .exclude(rating__lt=1)\
                      .order_by('-rating')\
                      .values_list('movie', flat=True)\
                      .distinct()

    return Movie.objects.filter(id__in = ids)

def readMatrixFromDB():
    numUsers = Settings.objects.get(name="numUsers").value
    numItems = Settings.objects.get(name="numItems").value
    shape = (numUsers, numItems)
    
    x = Rating.objects.all().exclude(isGuessed=True)
    mat = np.zeros(shape)
    for i in x:
       mat[i.user-1, i.movie_id-1] = i.rating
    return mat

def writeMatrixToDB(original, new):
    guessed = np.transpose(np.nonzero(original == 0))
    
    newRatings = []
    for (user, movie) in guessed:
        rat = Rating(movie_id=movie+1, user=user+1, rating=new[user,movie], isGuessed=True)
        newRatings.append(rat)

    Rating.objects.bulk_create(newRatings)

def background(timeout=10):
    def wraps(func):
        def _cb():
            while True:
                time.sleep( timeout )
                func()
        
        th = threading.Thread( target=_cb )
        th.daemon = True
        th.start()
    return wraps

def start():
    K = 2
    dbLock = threading.Lock()

    @background(100)
    def factor_matrix():
        with dbLock:
            print("[INFO] factorising matrix")
            orig = readMatrixFromDB()
            fact = factor_matrix_impl(orig.copy(), K)
            writeMatrixToDB(orig, fact)

    @background(10000)
    def dedup():
        ##Manually remove any duplicates. This lets us use the 'bulk_create' above without any issues
        with dbLock:
            print("[INFO] deduping db")

            unique_fields = ('movie_id', 'user')
            duplicates = Rating.objects\
                .values(*unique_fields)\
                .order_by()\
                .annotate(max_id=Max('id'), 
                          count_id=Count('id'))\
                .filter(count_id__gt=1)

            for duplicate in duplicates:
                Rating.objects.filter(**{x: duplicate[x] for x in unique_fields})\
                    .exclude(id=duplicate['max_id']).delete()

