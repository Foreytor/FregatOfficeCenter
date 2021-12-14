from django import forms
from django.forms.widgets import TextInput, TimeInput
from .models import Parkings, ParkingsTime
from datetime import datetime
from .validators import validatorIntervalTimes
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = 'date'


class ParkingReservationForm(forms.Form):
    parking_id = forms.CharField(widget=TextInput(
                                 attrs={'style': 'display:none'}))
    startDate = forms.DateField(widget=DateInput, label='Дата начала')
    startTime = forms.TimeField(widget=TimeInput(
                                attrs={'type': 'time'}), label='Время начала')
    stopDate = forms.DateField(widget=DateInput, label='Дата завершения')
    stopTime = forms.TimeField(widget=TimeInput(
                               attrs={'type': 'time'}),
                               label='Время завершения')
    fields = ['nametest', 'nametestt', 'StopDate', 'StopTime', 'test', ]

    def clean(self):
        cleaned_data = super().clean()
        parking_id = cleaned_data.get('parking_id')

        StartDateTime = datetime.combine(cleaned_data.get('startDate'),
                                         cleaned_data.get('startTime'))

        StoptDateTime = datetime.combine(cleaned_data.get('stopDate'),
                                         cleaned_data.get('stopTime'))

        if StartDateTime >= StoptDateTime:
            raise ValidationError("Дата окончания не может быть больше \
                                  даты начала")

        if not validatorIntervalTimes(parking_id, StartDateTime,
                                      StoptDateTime):
            raise ValidationError("Этот интервал занят")


class ParkingTimeUpdateForm(forms.ModelForm):
    class Meta:
        model = ParkingsTime
        fields = ['starDateTime', 'stopDateTime', ]

    def clean(self):
        cleaned_data = super(ParkingTimeUpdateForm, self).clean()

        StartDateTime = cleaned_data.get('starDateTime')

        StoptDateTime = cleaned_data.get('stopDateTime')

        if StartDateTime >= StoptDateTime:
            raise ValidationError("Дата окончания не может \
                                  быть больше даты начала")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['starDateTime'].widget.attrs. \
            update({'class': 'form-control'})
        self.fields['stopDateTime'].widget.attrs. \
            update({'class': 'form-control'})


class ParkingUpdateForm(forms.ModelForm):
    class Meta:
        model = Parkings
        fields = ['parkingName', 'description', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parkingName'].widget.attrs. \
            update({'class': 'form-control'})
        self.fields['description'].widget.attrs. \
            update({'class': 'form-control'})


class ParkingAddForm(forms.ModelForm):
    class Meta:
        model = Parkings
        fields = ['parkingName', 'description', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parkingName'].widget.attrs. \
            update({'class': 'form-control'})
        self.fields['description'].widget.attrs. \
            update({'class': 'form-control'})
