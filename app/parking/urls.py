"""FregatOfficeCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import Index, ParkingDetal, ParkingTimeCreate, \
    ParkingCreate, ParkingUpdate, ParkingDelete, \
    ParkingTimeUpdate, ParkingTimeDelete


urlpatterns = [
    path('', Index.as_view(), name="home"),
    path('parking/<int:pk>/delete/',
         ParkingDelete.as_view(), name='PlaceDelete'),
    path('parking/<int:pk>/deletetime/',
         ParkingTimeDelete.as_view(), name='PlaceTimeDelete'),
    path('parking/<int:pk>/',
         ParkingDetal.as_view(), name='ParkingDetal'),
    path('parking/add/',
         ParkingTimeCreate.as_view(), name='ParkingAdd'),
    path('parking/placeadd/',
         ParkingCreate.as_view(), name='PlaceAdd'),
    path('parking/placeedit/<int:pk>',
         ParkingUpdate.as_view(), name='PlaceEdir'),
    path('parking/timeedit/<int:pk>',
         ParkingTimeUpdate.as_view(), name='timeEdir'),
]
