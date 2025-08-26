from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user_phone_number", "department", "created_at")
    search_fields = ("name", "user_phone_number", "department", "complaint_message")
    list_filter = ("department", )
    ordering = ("-created_at",)
