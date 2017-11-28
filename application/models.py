from django.db import models
from django.forms import ModelForm

# Create your models here.
class Movie(models.Model):
  id          = models.IntegerField(primary_key=True)
  title       = models.CharField(max_length = 256)
  link        = models.CharField(max_length = 256)
  image       = models.CharField(max_length = 256)
  director    = models.CharField(max_length = 256)
  actor       = models.CharField(max_length = 256)
  description = models.CharField(max_length = 1024)

  def __str__(self):
    return "id:{} title:{}".format(self.id, self.title)
              
class Rating(models.Model):
  movie = models.ForeignKey('Movie')
  user = models.IntegerField()
  rating = models.IntegerField(default=0)
  isGuessed = models.BooleanField(default=False)

  def __str__(self):
    res = "User:{} Movie:{} Rating:{}"
    if self.isGuessed:
      res += " Guessed"

    return res.format(self.user, self.movie, self.rating)


class RatingForm(ModelForm):
  class Meta:
    model = Rating
    fields = ['movie', 'rating']

  def __str__(self):
    return "model"


class Settings(models.Model):
  name = models.CharField(max_length=256)
  value = models.IntegerField()

  def __str__(self):
    return "({} : {})".format(self.name, self.value)
