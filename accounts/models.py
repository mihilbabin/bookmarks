from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    following = models.ManyToManyField('self', through='Relationship', related_name='followers', symmetrical=False)

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(pk=self.pk)
            if this.photo != self.photo:
                this.photo.delete(save=False)
        except Profile.DoesNotExist:
            pass
        super(Profile, self).save(*args, **kwargs)
    def __str__(self):
        return "Profile for user {}".format(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_delete, sender=Profile)
def profile_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)


class Relationship(models.Model):
    user_from = models.ForeignKey(Profile, related_name='rel_from_set')
    user_to = models.ForeignKey(Profile, related_name='rel_to_set')
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)
