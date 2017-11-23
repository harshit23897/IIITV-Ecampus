from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import AssignmentSubmission, UserProfile

class AssignmentSubmissionForm(ModelForm):
    # def is_valid(self):
    #     valid = super(AssignmentSubmissionForm, self).is_valid()
    #     if not valid:
    #         return valid

    class Meta:
        model = AssignmentSubmission
        fields = ('file', )

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name' )


class EditProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('date_of_birth','email','city','phone','image' )