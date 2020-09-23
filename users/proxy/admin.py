from django.contrib import admin

from .models import Upstreams


class UpstreamAdmin(admin.ModelAdmin):
    display_list = ('id', 'path', 'upstream')


admin.site.register(Upstreams, UpstreamAdmin)
