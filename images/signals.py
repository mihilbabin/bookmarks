from django.dispatch import receiver
from django.db.models.signals import pre_delete, m2m_changed
from .models import Image
@receiver(pre_delete, sender=Image)
def profile_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)

@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
