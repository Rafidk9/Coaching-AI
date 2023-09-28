from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    recordings_given = models.IntegerField(default=0)
    last_recording_date = models.DateField(null=True, blank=True)

class Batch(models.Model):
    name = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50)

class ClassRecording(models.Model):
    link = models.URLField()
    date = models.DateField()
    topic = models.CharField(max_length=200)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

class AccessControl(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_recording = models.ForeignKey(ClassRecording, on_delete=models.CASCADE)
    access_date = models.DateField()