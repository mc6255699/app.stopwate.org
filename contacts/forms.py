from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Row, Column, Div, Field, Layout, HTML
from crispy_forms.bootstrap import  FormActions, FieldWithButtons, StrictButton

from django import forms
from .models import Contact
from .models import Organization

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 
            'last_name', 
            'job_title',
            'phone_number',
            'email',
            'organization',
            'owner'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@domain.com',
                'required': True,
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+1234567890',
                'pattern': r'^\+?1?\d{9,15}$',
                'title': 'Enter phone number in format +999999999. Up to 15 digits allowed.'
            }),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Layout with Bootstrap 5 grid and labels
        self.helper = FormHelper()  
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            
            Row(
                Column(Field('first_name'), css_class='col-md-6 mb-3'),
                Column(Field('last_name'), css_class='col-md-6 mb-3'),
            ),
            Row(
                Column(Field('job_title'), css_class='col-md-6 mb-3'),
                Column(Field('phone_number'), css_class='col-md-6 mb-3'),
            ),
            Field('email'),
            Row(
                Column(Field('organization'), css_class='col-md-6 mb-3'),
                Column(Field('owner'), css_class='col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', 'Save Contact', css_class='btn btn-primary')
            )
        )

class ContactFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Name')
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=False,
        empty_label='Any Organization'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'mb-4'
        self.helper.layout = Row(
            Column(Field('name'), css_class='col-md-4 mb-2'),
            Column(Field('organization'), css_class='col-md-4 mb-2'),
            Column(
                FormActions(Submit('filter', 'Filter', css_class='btn btn-primary mt-1')),
                css_class='col-md-4 d-flex align-items-center'
            ),
        )
