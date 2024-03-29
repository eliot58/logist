from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ["fullName", "name", "phone_number", "is_free"]

@admin.register(Logist)
class LogistAdmin(admin.ModelAdmin):
    list_display = ["fullName", "phone_number"]


class FileInline(admin.StackedInline):
    model = FileModel
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [FileInline]
    list_display = ["o_name", "plan_date", "date_logist", "qu", "sqr", "address", "floor", "c_name", "s_name"]

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["id","author_name"]

    @admin.display(ordering = "author__fullName", description = "Автор")
    def author_name(self, obj): 
        return obj.author.fullName
    
    
@admin.register(LogEntry)
class LogAdmin(admin.ModelAdmin):
    list_display = ["action_time", "user", "content_type", "object_repr", "__str__"]