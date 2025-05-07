from django.db import models

# define the first model (we will add this to our database)
class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
