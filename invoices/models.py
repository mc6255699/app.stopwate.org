from django.db import models
from django.contrib.auth.models import User

class Invoice(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    
    # Original uploaded file
    uploaded_pdf = models.FileField(upload_to='invoices/originals/')
    
    # The stamped version with the cover page
    stamped_pdf = models.FileField(upload_to='invoices/stamped/', blank=True, null=True)
    
    # Optional: for future Textract integration
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extracted_json = models.JSONField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.owner.username})"
