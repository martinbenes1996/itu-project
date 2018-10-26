from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Webpage(models.Model):
    name = models.CharField(max_length=64, default='New Webpage')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # For description of structure, I think about using the XSL file with a name including primary key from the database.
    # Therefore it should be easy with access to the database to reach the file easily.
    # There should be everything

    @classmethod
    def getWebpages(cls, user):
        l = []
        for w in cls.objects.all():
            if w.user.id == user.id:
                l.append(w.id)
        return cls.objects.filter(pk__in=l).values()
        

