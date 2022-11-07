import datetime

from api_office.models import Holiday
from api_office.services import HolidayService
from rest_framework import serializers


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"

    def to_representation(self, obj):
        today = datetime.date.today()
        if obj.repeat:
            start_date = datetime.datetime.strptime(str(obj.start_date), "%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(obj.end_date), "%Y-%m-%d")
            start_year = int(0 if obj.start_year is None else obj.start_year)
            end_year = int(0 if obj.end_year is None else obj.end_year)

            if obj.end_year > start_year:
                new_count = end_year - today.year
                step = obj.count - new_count
                obj.start_date = obj.start_date.replace(year=start_date.year + step)
                obj.end_date = obj.end_date.replace(year=end_date.year + step)
                obj.count = new_count
            else:
                new_count = start_year + int(obj.count) - today.year
                obj.start_date = obj.start_date.replace(year=today.year)
                obj.end_date = obj.end_date.replace(year=today.year)
                obj.count = new_count
        return super().to_representation(obj)

    def create(self, validated_data):
        if not validated_data.get("calendar_id"):
            calendar = HolidayService.create_event(validated_data)
            validated_data["calendar_id"] = calendar.get("id")
        return Holiday.objects.create(**validated_data)

    def update(self, instance, validated_data):
        HolidayService.update_event(instance, validated_data)
        return super().update(instance, validated_data)

    def validate(self, data):
        if data["repeat"]:
            start_date = datetime.datetime.strptime(str(data["start_date"]), "%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(data["end_date"]), "%Y-%m-%d")
            data["start_year"] = start_date.year
            data["end_year"] = end_date.year + int(
                0 if data["count"] is None else data["count"]
            )
        else:
            data["start_year"] = None
            data["end_year"] = None
            data["count"] = None

        return data
