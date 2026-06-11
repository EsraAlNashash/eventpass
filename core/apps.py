from django.apps import AppConfig


def _create_default_superuser(sender, **kwargs):
    """
    Runs once after every migrate. Creates a superuser only when none exists.
    Credentials can be overridden via Render environment variables.
    """
    from django.contrib.auth.models import User
    import os

    if User.objects.filter(is_superuser=True).exists():
        return

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'esra')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'omar@125')
    email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'[EventPass] Superuser "{username}" created automatically.')


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(_create_default_superuser, sender=self)
