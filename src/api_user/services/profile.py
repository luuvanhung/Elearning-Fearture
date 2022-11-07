from api_base.services import BaseService
from api_user.models import Profile
from api_user.serializers import ProfileSerializers


class ProfileService(BaseService):
    @classmethod
    def update_list_auto_booking(cls, profiles, status):
        updated_profiles = [Profile(id=profile.get("profile_id"), veggie=profile.get("veggie"), auto_booking_lunch=status) for profile in profiles]
        return Profile.objects.bulk_update(updated_profiles, ["auto_booking_lunch", "veggie"])

    @classmethod
    def update_slack_id_by_profile_id(cls, profile_id, slack_id):
        return Profile.objects.filter(pk=profile_id).update(slack_id=slack_id)

    @classmethod
    def get_profile_by_slack_id(cls, slack_id: str):
        return Profile.objects.filter(slack_id=slack_id).first()

    @classmethod
    def get_profile_by_email(cls, personal_email):
        return Profile.objects.filter(personal_email=personal_email).first()

    @classmethod
    def get_profile_by_user_id(cls, user_id):
        return Profile.objects.filter(user_id=user_id).first()

    @classmethod
    def get_all_profile(cls):
        profiles = Profile.objects.all()
        profile_serializers = ProfileSerializers(profiles, many=True)
        return profile_serializers.data
