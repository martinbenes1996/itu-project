from django.db import models
from django.contrib.auth.models import User

class Webpage(models.Model):
    name = models.CharField(max_length=64, default='New Webpage')
    url = models.URLField()
    webpages = models.ManyToManyField(User)
    # For description of structure, I think about using the XSL file with a name including primary key from the database.
    # Therefore it should be easy with access to the database to reach the file easily.
    # There should be everything

