import calendar
from datetime import date, datetime

from api_user.models import Profile
from api_user_lunch.models import UserLunch
from api_user_lunch.services import UserLunchServices
from api_workday.services.send_notification_slack import SendNotificationSlack
from common.constants.workday_constants import Workday


def set_lunch_auto_next_month():
    profiles = Profile.objects.filter(auto_booking_lunch=True)
    list_user_lunches = []
    start_day = Workday.FIRST_DAY + 1
    month = datetime.now().month + 1
    year = datetime.now().year
    today = datetime.now().date()
    if month > 12:
        year += 1
        month = 1
    total_days_month = calendar.monthrange(year, month)[1]
    for profile in profiles:
        for day in range(start_day, total_days_month + 1):
            date = str(year) + "-" + str(month) + "-" + str(day)
            convert_to_datetime = datetime.strptime(date, "%Y-%m-%d").date()
            week_day = convert_to_datetime.weekday()
            if UserLunchServices.is_weekday(day=week_day):
                continue
            if today <= convert_to_datetime:
                user_lunch = UserLunch.objects.filter(date=date, profile=profile)
                if not user_lunch.exists():
                    if profile.veggie and UserLunchServices.is_lunar_day(
                        convert_to_datetime
                    ):
                        list_user_lunches.append(
                            UserLunch(date=date, profile=profile, has_veggie=True)
                        )
                    else:
                        list_user_lunches.append(UserLunch(date=date, profile=profile))
    return UserLunch.objects.bulk_create(list_user_lunches)

def send_notification_about_lunch():
    today = date.today()
    data = UserLunch.objects.filter(date=today).values()
    lunches = 0
    veggies = 0
    if data:
        for d in data:
            if d.get('has_veggie'):
                veggies+=1
            else:
                lunches+=1
    SendNotificationSlack.send_notification_about_lunch(number_veggies=veggies,number_lunches=lunches)
