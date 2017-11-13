from django.forms import ModelForm
from .models import AssignmentSubmission

class AssignmentSubmissionForm(ModelForm):
    # def is_valid(self):
    #     valid = super(AssignmentSubmissionForm, self).is_valid()
    #     if not valid:
    #         return valid

    class Meta:
        model = AssignmentSubmission
        fields = ('file', )