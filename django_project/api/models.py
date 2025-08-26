from django.db import models


class Complaint(models.Model):
    name = models.CharField(max_length=100, blank=False)
    user_phone_number = models.CharField(max_length=100, blank=False, null=False)
    user_address = models.TextField(blank=False)
    complaint_message = models.TextField(blank=False, null=False)
    department = models.CharField(max_length=100)
    raw_conversation = models.TextField(blank=False, null=False)
    raw_complaint_json = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
