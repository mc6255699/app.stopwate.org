from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['code', 'note', 'uploaded_pdf']
        labels = {
            'uploaded_pdf': 'Upload PDF',
        }
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional notes...'}),
            'code': forms.TextInput(attrs={'placeholder': 'Enter code'}),
        }
