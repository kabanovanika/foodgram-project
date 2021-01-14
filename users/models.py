# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=150)
#     bio = models.TextField()
#
#     def __str__(self):
#         return self.user.username
#
#
# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

# from django.db import models
# from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
#
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class UserRoles(models.TextChoices):
#     USER = 'user'
#     ADMIN = 'admin'
#
#
# class User(AbstractUser):
#     """
#     This is custom class for create User model, where email field instead
#     username field.
#     """
#     name = models.CharField(_('name'), max_length=40, unique=False)
#     username = models.CharField(_('username'),
#                                 max_length=30,
#                                 blank=True,
#                                 unique=True)
#     email = models.EmailField(_('email address'), unique=True)
#     role = models.CharField(
#         verbose_name='Роль пользователя',
#         max_length=10,
#         choices=UserRoles.choices,
#         default=UserRoles.USER,
#     )
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ('name',)
#
#     @property
#     def is_admin(self):
#         """
#         Function for quick change property 'role' of User model.
#         """
#         return (self.role == UserRoles.ADMIN or self.is_superuser
#                 or self.is_staff)
#
#     def get_full_name(self):
#         """
#         Function for concatenate full name of user, use first and last name.
#         """
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
