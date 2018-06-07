from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateOfBirth = models.DateField(null=True, blank=True)
    profilePhoto = models.ImageField(null=True, blank=True, upload_to='static')
    SEX = [('F', 'Female'),('M', 'Male')]
    sex = models.CharField(null=True, choices=SEX, max_length=1, default='F')
    lookingFor = models.CharField(null=True, choices=SEX, max_length=1, default='M')

    def __str__(self):
        return str(self.id)

class Rating(models.Model):
    ratingUser = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ratingUser')
    ratedUser = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ratedUser')
    like = models.BooleanField()

    class Meta:
        unique_together = ('ratingUser', 'ratedUser')
    
    def __str__(self):
        return str(self.ratingUser) + ' ' + str(self.ratedUser) + ' ' + str(self.like)

class Match(models.Model):
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user2')

    class Meta:
        unique_together = ('user1', 'user2')
        unique_together = ('user2', 'user1')
    def __str__(self):
        return str(self.user1) + ' ' + str(self.user2)

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient')
    text = models.CharField(max_length=280)
    sentDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sender) + ' ' + str(self.recipient) + ' ' + self.text

@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()