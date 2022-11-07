import datetime
from calendar import monthrange
from datetime import timedelta
from typing import Dict, List, Tuple

from api_user_lunch.models import UserLunch
from lunarcalendar import Converter, Solar


class UserLunchServices:
    @classmethod
    def get_users_lunch(cls, profile):
        users_lunch = UserLunch.objects.filter(profile=profile)
        if not users_lunch.exists():
            return []
        return users_lunch

    @classmethod
    def create(cls, serializer, profile, date):
        today = datetime.date.today()
        convert_to_datetime = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        week_day = convert_to_datetime.weekday()
        if cls.is_weekday(day=week_day):
            raise Exception("Cant set lunch at weekend")
        if datetime.datetime.strptime(
            str(today), "%Y-%m-%d"
        ) <= datetime.datetime.strptime(str(date), "%Y-%m-%d"):
            if UserLunch.objects.filter(date=date, profile=profile).exists():
                raise Exception(f"The lunch have been created with date {date}")
            return serializer.save(profile=profile)
        raise Exception("Create Error")

    @classmethod
    def create_many(cls, data, list_dates, profile):
        list_user_lunches = []
        if not list_dates:
            raise Exception("list_dates are empty")
        today = datetime.date.today()
        for date in list_dates:
            convert_to_datetime = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            week_day = convert_to_datetime.weekday()
            if cls.is_weekday(day=week_day):
                continue
            if datetime.datetime.strptime(
                str(today), "%Y-%m-%d"
            ) <= datetime.datetime.strptime(str(date), "%Y-%m-%d"):
                user_lunch = UserLunch.objects.filter(date=date, profile=profile)
                if not user_lunch.exists():
                    has_veggie = data.get("has_veggie") and cls.is_lunar_day(convert_to_datetime)
                    list_user_lunches.append(
                        UserLunch(
                            date=date,
                            profile=profile,
                            has_veggie=has_veggie,
                        )
                    )
        return UserLunch.objects.bulk_create(list_user_lunches)

    @classmethod
    def create_many_for_employees(cls, data_user_lunches: List[Dict]):
        user_lunches_create = []
        user_lunches_update = []

        # get list dates
        start_date = datetime.datetime.now()
        year = start_date.year
        month = start_date.month
        last_day_of_month = monthrange(year, month)[1]
        if start_date.hour >= 9:
            start_date += timedelta(days=1)

        # check today is the last day of the year
        if start_date.year != year:
            return
        dates = [datetime.date(year, month, day) for day in range(start_date.day, last_day_of_month + 1)]
        profile_ids = [data_user_lunch.get("profile_id") for data_user_lunch in data_user_lunches]
        exist_user_lunches = UserLunch.objects.filter(
            date__in=dates,
            profile_id__in=profile_ids
        )
        check_exist_user_lunch = {}
        for user_lunch in exist_user_lunches:
            check_exist_user_lunch.update({(user_lunch.date, str(user_lunch.profile_id)): user_lunch})
        for date in dates:
            # check weekend
            if cls.is_weekday(day=date.weekday()):
                continue
            for data_user_lunch in data_user_lunches:
                has_veggie = data_user_lunch.get("veggie") if cls.is_lunar_day(date) else False
                profile_id = str(data_user_lunch.get("profile_id"))
                user_lunch = check_exist_user_lunch.get((date, profile_id))
                if user_lunch:
                    if has_veggie != user_lunch.has_veggie:
                        user_lunch.has_veggie = has_veggie
                        user_lunches_update.append(user_lunch)
                else:
                    user_lunches_create.append(
                        UserLunch(
                            date=date,
                            profile_id=profile_id,
                            has_veggie=has_veggie
                        )
                    )

        UserLunch.objects.bulk_update(user_lunches_update, ["has_veggie"])
        UserLunch.objects.bulk_create(user_lunches_create)
        return

    @classmethod
    def create_many_by_admin(cls, list_data):
        if not list_data:
            raise Exception("list_data is empty")
        list_user_lunches = []
        for data in list_data:
            user_lunch = UserLunch.objects.filter(date=data['date'], profile=data['profile'])
            if not user_lunch.exists():
                list_user_lunches.append(
                    UserLunch(date=data['date'], profile=data['profile'], has_veggie=data['has_veggie'] and cls.is_lunar_day(data['date']))
                )
        results = UserLunch.objects.bulk_create(list_user_lunches)
        return results

    @classmethod
    def is_lunar_day(cls, date):
        solar = Solar(date.year, date.month, date.day)
        lunar = Converter.Solar2Lunar(solar)
        if lunar.day == 1 or lunar.day == 15:
            return True
        return False

    @classmethod
    def is_weekday(cls, day):
        return True if day in [5, 6] else False

    @classmethod
    def set_veggie(cls, profile):
        now = datetime.datetime.now()
        last_day = now.replace(day=monthrange(now.year, now.month)[1])
        list_existed_lunar = []
        user_lunches = UserLunch.objects.filter(
            date__gte=now, date__lte=last_day, profile=profile
        ).values_list("date", flat=True)
        if not user_lunches.exists():
            list_user_lunches = []
            list_lunar_days = []
            step = datetime.timedelta(days=1)
            while now <= last_day:
                week_day = now.weekday()
                if cls.is_weekday(day=week_day):
                    now += step
                    continue
                if cls.is_lunar_day(date=now):
                    list_lunar_days.append(now)
                    list_user_lunches.append(
                        UserLunch(date=now, profile=profile, has_veggie=True)
                    )
                now += step
            if not list_lunar_days:
                raise Exception("Not found lunar day")
            return UserLunch.objects.bulk_create(list_user_lunches)
        for date in user_lunches:
            if cls.is_lunar_day(date=date):
                list_existed_lunar.append(date)
        UserLunch.objects.filter(profile=profile, date__in=list_existed_lunar).update(
            has_veggie=True
        )
        if not list_existed_lunar:
            raise Exception("Not found lunar day")
        return

    @classmethod
    def get_object(cls, pk):
        try:
            user_lunch = UserLunch.objects.get(id=pk)
            return user_lunch
        except UserLunch.DoesNotExist:
            raise Exception("Lunch is empty")

    @classmethod
    def update(cls, serializer, pk, date):
        user_lunch_instance = cls.get_object(pk)
        get_user_lunch = UserLunch.objects.filter(date=date).first()
        lunch_date = user_lunch_instance.date
        date_instance = datetime.date(
            lunch_date.year, lunch_date.month, lunch_date.day
        ).strftime("%Y-%m-%d")
        if date and date != date_instance and get_user_lunch is not None:
            raise Exception(f"Lunch have been updated with date {date}")
        return serializer.save()

    @classmethod
    def delete(cls, pk):
        today = datetime.date.today()
        lunch = UserLunch.objects.filter(id=pk, date__gte=today)
        if not lunch.exists():
            raise Exception("Can not delete lunch with date lunch little than now")
        return lunch.delete()

    @classmethod
    def bulk_update_veggie(cls, data_user_lunches: List[Dict]):
        update_user_lunches = [UserLunch(
            id=data.get("id"),
            has_veggie=not data.get("has_veggie")
        ) for data in data_user_lunches]
        user_lunches = UserLunch.objects.bulk_update(update_user_lunches, ["has_veggie"])
        return user_lunches

    @classmethod
    def bulk_delete(cls, user_lunch_ids: List[str]) -> Tuple:
        user_lunches = UserLunch.objects.filter(id__in=user_lunch_ids).delete()
        return user_lunches
