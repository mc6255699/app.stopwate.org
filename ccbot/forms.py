from django import forms
from .models import CCRequest, CCName

from django import forms

CC_CHOICES = {
    "CC-ALMA":     "aypa6f6cngmjs7orzrexcb76ne",
    "CC-ARLISSS":  "azsbc7fnhfz2b7lhpqvmqiwbum",
    "CC-Mike":     "mrlzyjgdckgwu2frchygu4r55q",
    "CC-PAT":      "474n7o42soe33u6wv4etbdcyly",
    "CC-JUSTIN":   "77bznv54n3hdzqrpyk4mhmoysu",
    "CC-ANGELINA": "t6icvh35cyogafuplltb4kc",
}

CC_CHOICES_TUPLES = [(v, k) for k, v in CC_CHOICES.items()]



class CCRequestForm(forms.ModelForm):
    credit_card_name = forms.ModelChoiceField(
        queryset=CCName.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Name on Card"
    )

    class Meta:
        model = CCRequest
        fields = ['description', 'vendor', 'amount', 'credit_card_name', 'it_approval']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe what is being purchased'
            }),
            'vendor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Amazon, Staples'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 123.45'
            }),
            # 'payment_code': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': ''
            # }),
        }
        labels = {
            'payment_code': 'Allocation Code (optional)',
            'vendor': 'Merchant Name',
            'it_approval': '   Yes I have written IT approval'
         }
        help_texts = {
            'it_approval': '💡 IT approval is required for all software/equipment purchases. If you do not have written approval, please contact Mike before any purchase.'
        }
          