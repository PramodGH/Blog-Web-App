from django.apps import AppConfig


class BlogAppConfig(AppConfig):
    name = 'blog_app'

    def ready(self):
        from . import signals