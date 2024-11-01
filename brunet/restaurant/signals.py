from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import Usuario

@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    user.ultima_sesion = timezone.now()
    user.save()
    print(f'Usuario {user.username} inició sesión a las {user.ultima_sesion}')

@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    print(f'Usuario {user.username} cerró sesión')
