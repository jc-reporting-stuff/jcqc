from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=50)
    headline = models.CharField(
        max_length=150, null=True, blank=True, verbose_name='Headline or Subject Line')
    styling = models.CharField(max_length=500, null=True, blank=True,
                               verbose_name='Inline CSS for styling (front page only)')
    content = models.TextField(max_length=5000)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
