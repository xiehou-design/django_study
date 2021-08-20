from django.db import models

class Classes(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    age = models.IntegerField()
    cls = models.ForeignKey('Classes')


class Teacher(models.Model):
    tname = models.CharField(max_length=32)
    """
    10
    """
    c2t = models.ManyToManyField('Classes')
