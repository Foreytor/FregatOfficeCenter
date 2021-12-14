from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from .models import Parkings, ParkingsTime
from .forms import ParkingReservationForm, \
    ParkingTimeUpdateForm, ParkingUpdateForm, ParkingAddForm
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


@method_decorator(login_required, name='dispatch')
class Index(UserPassesTestMixin, ListView):
    """Home page view"""
    model = Parkings
    template_name = "parking/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = self.request.user.groups.filter(name='Manager').exists()
        context['manager'] = manager
        return context

    def test_func(self):
        if self.request.user.groups.filter(name='Manager').exists() \
           or self.request.user.groups.filter(name='Employee').exists():
            result = True
        else:
            result = False
        return result


@method_decorator(login_required, name='dispatch')
class ParkingDetal(UserPassesTestMixin, DetailView):
    """View for creating and displaying the pre-programmed time"""
    model = Parkings
    template_name = "parking/parkingDetal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_parking = context['object'].id
        context['ParkingsTimeList'] = ParkingsTime.objects. \
            filter(parkingName_id__exact=id_parking)
        form = ParkingReservationForm()
        form.fields['parking_id'].label = ''
        form.fields['parking_id'].initial = id_parking
        context['parkingReservationForm'] = form
        manager = self.request.user.groups.filter(name='Manager').exists()
        context['manager'] = manager
        employee = self.request.user.groups.filter(name='Employee').exists()
        context['employee'] = employee
        if 'statusAdd' in self.request.session:
            context['statusAdd'] = self.request.session['statusAdd']
            del self.request.session['statusAdd']
        return context

    def test_func(self):
        if self.request.user.groups.filter(name='Manager').exists() \
           or self.request.user.groups.filter(name='Employee').exists():
            result = True
        else:
            result = False
        return result


@method_decorator(login_required, name='dispatch')
class ParkingTimeCreate(CreateView):
    """Time reservation"""
    model = ParkingsTime
    fields = ['starDateTime', 'stopDateTime', ]

    template_name = 'parking/parkingDetal.html'

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def post(self, request, *args, **kwargs):
        form = ParkingReservationForm(request.POST)
        parkings_id = int(form['parking_id'].value())
        if form.is_valid():
            parkingTime = ParkingsTime()
            parkingTime.user = request.user
            parkingTime.parkingName = Parkings.objects.get(id=parkings_id)
            starDateTimeStr = '{} {}'.format(form['startDate'].value(),
                                             form['startTime'].value())
            stopDateTimeStr = '{} {}'.format(form['stopDate'].value(),
                                             form['stopTime'].value())
            parkingTime.starDateTime = datetime.strptime(starDateTimeStr,
                                                         '%Y-%m-%d %H:%M')
            parkingTime.stopDateTime = datetime.strptime(stopDateTimeStr,
                                                         '%Y-%m-%d %H:%M')
            parkingTime.save()
            request.session['statusAdd'] = 'Место забронированно'
            return redirect(reverse('ParkingDetal', args=[parkings_id]))
        else:
            request.session['statusAdd'] = form.errors['__all__'][0]
            return redirect(reverse('ParkingDetal', args=[parkings_id]))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ParkingCreate(UserPassesTestMixin, CreateView):
    """Creating a parking space"""
    model = Parkings
    form_class = ParkingAddForm

    template_name = 'parking/parkingPlaceAdd.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


@method_decorator(login_required, name='dispatch')
class ParkingUpdate(UserPassesTestMixin, UpdateView):
    """View for changing parking space"""
    model = Parkings
    template_name = 'parking/parkingPlaceEdit.html'
    form_class = ParkingUpdateForm
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


@method_decorator(login_required, name='dispatch')
class ParkingDelete(UserPassesTestMixin, DeleteView):
    """View to remove parking space"""
    model = Parkings
    template_name = 'parking/parkingPlaceDelete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


@method_decorator(login_required, name='dispatch')
class ParkingTimeUpdate(UserPassesTestMixin, UpdateView):
    """Browsing change view"""
    model = ParkingsTime
    template_name = 'parking/parkingTimeEdit.html'
    form_class = ParkingTimeUpdateForm
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


@method_decorator(login_required, name='dispatch')
class ParkingTimeDelete(UserPassesTestMixin, DeleteView):
    """Browsing Removal View"""
    model = ParkingsTime
    template_name = 'parking/parkingTimeDelete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()
