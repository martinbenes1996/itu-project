from django.db import models

class Webpage(models.Model):
    name = models.CharField(max_length=64, default='New Webpage')
    url = models.URLField()
    # For description of structure, I think about using the XSL file with a name including primary key from the database.
    # Therefore it should be easy with access to the database to reach the file easily.
    # There should be everything

class User(model.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=64, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=64)
    birthday = models.DateTimeField('date of a birth', blank=True)

    webpages = models.ManyToManyField(Webpage)