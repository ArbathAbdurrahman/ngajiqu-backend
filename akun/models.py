from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

def user_directory_path(instance, filename):
    return f'images/user_{instance.user.id}/profile_images_{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Biodata
    description = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    contact = models.EmailField(blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ 
    Membuat objek UserProfile setiap kali User baru disimpan
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(pre_save, sender=UserProfile)
def delete_old_profile_image_on_update(sender, instance, **kwargs):
    """
    Hapus gambar setiap user update foto profile baru
    """
    if not instance.pk:
        return
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        return
    old_image = old_instance.profile_image
    if old_image and old_image != instance.profile_image and old_image.storage.exists(old_image.name):
        old_image.delete(save=False)