from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=300)
    url = models.TextField(null=True)
    source = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)
    type = models.IntegerField(null=True)

    def __str__(self):
        return self.headline

