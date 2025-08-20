from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Submit, Field, ButtonHolder, HTML
from crispy_forms.bootstrap import  FormActions, FieldWithButtons, StrictButton
from django import forms
from .models import *
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'job_title', 'phone_number', 'email', 'organization', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # Order orgs nicely; adjust as you like
        self.fields['organization'].queryset = Organization.objects.order_by('name')
        self.fields['organization'].empty_label = "Select an organization (optional)"

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6 mb-3'),
                Column('last_name', css_class='col-md-6 mb-3')
            ),
            Row(
                Column('job_title', css_class='col-md-6 mb-3'),
                Column('phone_number', css_class='col-md-6 mb-3')
            ),
           Row(
                Column('email', css_class='col-md-6 mb-3'),
                Column('organization', css_class='col-md-6 mb-3')
            ),
            'note',
            ButtonHolder(
                HTML("""
                     <div class="d-flex justify-content-end">
                    <button type="submit" class="btn btn-sm btn-outline-success" title="Save">
                         <i class="fas fa-floppy-disk"></i>
                    </button>
                     </div>
                """)
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
        fields = ["name", "description", "active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            Submit("submit", "Save", css_class="btn btn-primary"),
        )


    # def clean_sublists(self):
    #     subs = self.cleaned_data.get("sublists")
    #     if self.instance and self.instance.pk and subs.filter(pk=self.instance.pk).exists():
    #         raise forms.ValidationError("A list cannot include itself as a sublist.")
    #     return subs
