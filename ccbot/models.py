from django.db import models
from decimal import Decimal  # Import this for precise decimal literals
from django.conf import settings  # For linking to the logged-in user (email)

class CCName(models.Model):
    cc_name = models.CharField(max_length=100)
    onepassword_id = models.CharField(max_length=100, verbose_name="1Password ID",unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.cc_name


class CCRequest(models.Model):
    description = models.TextField(help_text="Describe the purchase in detail.")
    vendor = models.CharField(max_length=100)
    credit_card_name = models.ForeignKey(CCName, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    requested_by = models.EmailField()  # Or: models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_code = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    it_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vendor} - {self.description[:30]}"
