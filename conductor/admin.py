from django.contrib import admin

from models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'got_results')

admin.site.register(Task, TaskAdmin)

class KVAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value', 'unpickled', 'expiration', 'expired')

admin.site.register(KV, KVAdmin)
