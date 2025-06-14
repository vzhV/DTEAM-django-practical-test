from django.contrib import admin
from .models import RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "method", "path", "remote_ip")
    search_fields = ("path", "remote_ip")
    list_filter = ("method",)
    readonly_fields = [f.name for f in RequestLog._meta.fields]
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
