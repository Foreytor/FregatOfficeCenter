from typing import List
from django.db.models.sql.where import OR
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Parkings, ParkingsTime
from .forms import ParkingReservationForm
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


@method_decorator(login_required, name='dispatch')
class Index(UserPassesTestMixin, ListView):
    model = Parkings
    template_name = "parking/index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        manager = self.request.user.groups.filter(name='Manager').exists()
        context['manager'] = manager
        return context

    def test_func(self):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.groups.filter(name='Employee').exists():
            result = True
        else:
            result = False
        return result

    
@method_decorator(login_required, name='dispatch')
class ParkingDetal(UserPassesTestMixin, DetailView):
    model = Parkings
    template_name = "parking/parkingDetal.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        id_parking = context['object'].id
        context['ParkingsTimeList'] = ParkingsTime.objects.filter(parkingName_id__exact=id_parking)
        form = ParkingReservationForm()
        form.fields['parking_id'].label = ''
        form.fields['parking_id'].initial = id_parking
        context['parkingReservationForm'] = form
        manager = self.request.user.groups.filter(name='Manager').exists()
        context['manager'] = manager     
        employee = self.request.user.groups.filter(name='Employee').exists()
        context['employee'] = employee
        return context
    

    #def post(self, request, *args, **kwargs):
    #    self.object = self.get_object()
    #    form = self.get_form()
    #    if form.is_valid():
    #        return self.form_valid(form)
    #    else:
    #        return self.form_invalid(form)


    def test_func(self):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.groups.filter(name='Employee').exists():
            result = True
        else:
            result = False
        return result


@method_decorator(login_required, name='dispatch')
class ParkingTimeCreate(CreateView):
    model = ParkingsTime
    fields = ['starDateTime', 'stopDateTime',]

    template_name = 'parking/parkingDetal.html'

    def get(self, request, *args, **kwargs):
        #print('+++++++========='+str(form['parking_id'].value()))
        return redirect('home')

    def post(self, request, *args, **kwargs):
        form = ParkingReservationForm(request.POST)
        parkings_id = int(form['parking_id'].value())
        if form.is_valid():
            parkingTime = ParkingsTime()
            parkingTime.user = request.user
            parkingTime.parkingName = Parkings.objects.get(id=parkings_id)
            starDateTimeStr = '{} {}'.format(form['startDate'].value(), form['startTime'].value())
            stopDateTimeStr = '{} {}'.format(form['stopDate'].value(), form['stopTime'].value())
            print('dsfgdsf' + starDateTimeStr)
            parkingTime.starDateTime = datetime.strptime(starDateTimeStr, '%Y-%m-%d %H:%M')
            parkingTime.stopDateTime = datetime.strptime(stopDateTimeStr, '%Y-%m-%d %H:%M')
            parkingTime.save()
        #return redirect('parking/' + str(parkings_id))
        return redirect(reverse('home'))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ParkingCreate(UserPassesTestMixin, CreateView):
    model = Parkings
    fields = ['parkingName', 'description',]

    template_name = 'parking/parkingPlaceAdd.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

@method_decorator(login_required, name='dispatch')
class ParkingUpdate(UserPassesTestMixin, UpdateView):
    model = Parkings
    fields = ['parkingName', 'description',]
    template_name = 'parking/parkingPlaceEdit.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

@method_decorator(login_required, name='dispatch')
class ParkingDelete(UserPassesTestMixin, DeleteView):
    model = Parkings
    template_name = 'parking/parkingPlaceDelete.html'
    success_url = reverse_lazy('home')


    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    #def get(self, request, *args, **kwargs):
    #    user = self.request.user
    #    self.object = self.get_object()
    #    context = self.get_context_data(object=self.object)
    #    return self.render_to_response(context)



@method_decorator(login_required, name='dispatch')
class ParkingTimeUpdate(UserPassesTestMixin, UpdateView):
    model = ParkingsTime
    fields = ['starDateTime', 'stopDateTime',]
    template_name = 'parking/parkingPlaceEdit.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    