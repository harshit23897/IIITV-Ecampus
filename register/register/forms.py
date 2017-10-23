from django import forms
from registration.forms import RegistrationFormUniqueEmail


class NewRegistrationForm(RegistrationFormUniqueEmail):

    # def __init__(self, *args, **kwargs):
    #     super(NewRegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        cleaned_data = super(NewRegistrationForm, self).clean_email()
        if "@iiitvadodara.ac.in" not in cleaned_data:
            raise forms.ValidationError("You must have a IIIT Vadodara email address to register.")
        return cleaned_data
