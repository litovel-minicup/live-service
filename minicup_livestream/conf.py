# coding=utf-8


def configure():
    import django
    from django.conf import settings as django_settings

    from minicup import settings

    django_settings.configure(settings)
    django.setup()
