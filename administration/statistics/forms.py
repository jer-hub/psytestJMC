from django.forms import ModelForm
from accounts.models import Profile
from iqtest.models import Result as IQResult
from django import forms
from django.utils import timezone

now = timezone.now()
year_range = list(range(now.year - 100, now.year + 1))
year_range.reverse()

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("sex", "educationlevel", "department", "program", "year")
        widgets = {
            "sex": forms.Select(attrs={
                "class": "form-select"
            }),
            "educationlevel": forms.Select(attrs={
                "class": "form-select"
            }),
            "department": forms.Select(attrs={
                "class": "form-select"
            }),
            "program": forms.Select(attrs={
                "class": "form-select"
            }),
            "year": forms.Select(attrs={
                "class": "form-select"
            }),
        }

    
class IQStatForm(ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super(IQStatForm, self).__init__(*args, **kwargs)
        self.fields.update(ProfileForm().fields)
    
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day"), years=year_range, attrs={
                                                                'class': 'form-select',
                                                                'required': True,
                                                            }))
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day"), years=year_range, attrs={
                                                                'class': 'form-select',
                                                                'required': True,
                                                            }))
    
    class Meta:
        model = IQResult
        fields = ["start_date", "end_date", "result"]
        