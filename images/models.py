from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.urlresolvers import reverse

class Image(models.Model):
    user = models.ForeignKey(User, related_name='images_created')
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def save(self, *args, **kwargs):
        try:
            this = Image.objects.get(pk=self.pk)
            if this.image != self.image:
                this.image.delete(save=False)
        except Image.DoesNotExist:
            pass
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
