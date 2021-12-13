from django import forms
from django.forms.widgets import TextInput, TimeInput
from .models import Parkings, ParkingsTime

class DateInput(forms.DateInput):
    input_type = 'date'

'''class ParkingReservationForm(forms.ModelForm):
    nametest = forms.DateTimeField(widget=DatePickerInput)
    class Meta:
        model = ParkingsTime
        fields = ['starDateTime', 'stopDateTime', 'nametest']
        widgets = {
            'nametest': DateTimePickerInput,
            'starDateTime': DateTimePickerInput,
            'stopDateTime': DateTimePickerInput,
        }
'''
class ParkingReservationForm(forms.Form):
    #nametest = forms.DateField(widget=forms.SelectDateWidget)
    parking_id = forms.CharField(widget=TextInput(attrs={'style': 'display:none'}))
    startDate = forms.DateField(widget=DateInput)
    startTime = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}))
    stopDate = forms.DateField(widget=DateInput)
    stopTime = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}))
    fields = ['nametest', 'nametestt', 'StopDate', 'StopTime', 'test',]