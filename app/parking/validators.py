from .models import ParkingsTime
from collections import namedtuple
import pytz


utc = pytz.UTC


def validatorIntervalTimes(parking_id, startDateTime, stopDateTime):

    listParkingsTime = ParkingsTime.objects. \
        filter(parkingName_id__exact=parking_id)
    Range = namedtuple('Range', ['start', 'end'])

    startDateTime = utc.localize(startDateTime)
    stopDateTime = utc.localize(stopDateTime)
    print(startDateTime)
    print(stopDateTime)
    inDatetime = Range(start=startDateTime, end=stopDateTime)
    if listParkingsTime:
        for i in listParkingsTime:
            latest_start = max(i.starDateTime, inDatetime.start)
            earliest_end = min(i.stopDateTime, inDatetime.end)
            print(i.starDateTime)
            print(i.stopDateTime)
            delta = (earliest_end - latest_start).days + 1
            overlap = max(0, delta)
            print('delta = ' + str(delta))
            if overlap > 0:
                return False
        return True
    else:
        return True
