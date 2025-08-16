from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Submit, Field
from crispy_forms.bootstrap import  FormActions, FieldWithButtons, StrictButton
from django import forms
from .models import *

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
            'owner', 
            'note'
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
            'note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Additional notes about the contact'}),
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
            Row(
                Column(Field('note'), css_class='col-md-12 mb-3'),
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

class ContactListForm(forms.ModelForm):
    class Meta:
        model = ContactList
        fields = ["name", "description", "active", "contacts", "sublists"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "contacts": forms.SelectMultiple(attrs={"class": "form-select", "size": 8}),
            "sublists": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Order pickers in a friendly way (adjust if your Contact fields differ)
        # Use all contacts when creating a new list, but only show current contacts when editing
        if self.instance and self.instance.pk:
            self.fields["contacts"].queryset = self.instance.contacts.all().order_by("last_name", "first_name")
        else:
            self.fields["contacts"].queryset = Contact.objects.all().order_by("last_name", "first_name")

        self.fields["sublists"].queryset = ContactList.objects.all().order_by("name")

        # Exclude self from sublists on edit to avoid self-reference
        if self.instance and self.instance.pk:
            self.fields["sublists"].queryset = self.fields["sublists"].queryset.exclude(pk=self.instance.pk)

        self.fields["contacts"].help_text = "Hold Ctrl/Cmd to select multiple."
        self.fields["sublists"].help_text = "Optional: include other contact lists."

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Fieldset(
                "Contact List",
                Row(
                    Column("name", css_class="col-md-6"),
                    Column("active", css_class="col-md-2 d-flex align-items-center"),
                    Column("description", css_class="col-md-12 mt-2"),
                ),
            ),
            Fieldset(
                "Members",
                Row(
                    Column("contacts", css_class="col-md-7"),
                    Column("sublists", css_class="col-md-5"),
                ),
            ),
            Submit("submit", "Save", css_class="btn btn-primary"),
        )

    def clean_sublists(self):
        subs = self.cleaned_data.get("sublists")
        if self.instance and self.instance.pk and subs.filter(pk=self.instance.pk).exists():
            raise forms.ValidationError("A list cannot include itself as a sublist.")
        return subs
