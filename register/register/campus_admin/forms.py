from django import forms
from .models import Registers,FeeReceipt


class ResultForm(forms.ModelForm):
    class Meta:
        model = Registers
        fields = ['grade']

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        length = len(grade)
        if length == 2:
            for i in range(0,length):
                if ord(grade[i])<65  or  ord(grade[i])>70:
                    raise forms.ValidationError("Invalid Data")
        else :
            raise forms.ValidationError("Invalid Data")


class FeeReceiptForm(forms.ModelForm):
    class Meta:
        model = FeeReceipt
        fields = ['receiptId','status']

    def clean_receiptId(self):
        receiptId = self.cleaned_data['receiptId']
        if FeeReceipt.objects.filter(receiptId = receiptId):
            raise forms.ValidationError("ReceiptId already exists")
