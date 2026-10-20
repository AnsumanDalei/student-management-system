from django.db import models

# Create your models here.

class Student(models.Model):

    COURSE_CHOICES = [
        ('Python', 'Python'),
        ('Django', 'Django'),
        ('AWS Cloud', 'AWS Cloud'),
        ('DevOps', 'DevOps'),
        ('Java', 'Java'),
        ('Data Science', 'Data Science'),
    ]

    name = models.CharField(max_length=100)
    profile_photo = models.ImageField(
    upload_to='student_photos/',
    blank=True,
    null=True
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,)
    address = models.TextField()
    course = models.CharField(max_length=30, choices=COURSE_CHOICES)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name
