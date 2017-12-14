from django.contrib import admin

from django.apps import AppConfig

from .models import *


class DefaultAppConfig(AppConfig):
    name = 'Semiconductor Lab'
    def ready(self):
        from django.contrib import admin
        from django.contrib.admin import sites

        class MyAdminSite(admin.AdminSite):
            site_header = '<h1>Semiconductor Lab</h1>'
            site_title = "Semiconductor Lab"
        mysite = MyAdminSite()
        admin.site = mysite
        sites.site = mysite

admin.AdminSite.site_header = 'Semiconductor Lab'

admin.AdminSite.site_title = 'Semiconductor Lab - admin'

admin.site.register(training)

admin.site.register(upload_groups)

admin.site.register(upload)

admin.site.register(xml_intensities)

