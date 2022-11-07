import uuid

from api_user.models import Profile, User


def get_user_from_profile(profile: Profile) -> User:
    user_profile: User = profile.user
    try:
        user = User.objects.get(pk=user_profile.id)
    except User.DoesNotExist:
        user = None
    return user


def get_user_from_profile_id(profile_id: uuid.UUID) -> User:
    try:
        profile: Profile = Profile.objects.get(pk=profile_id)
        user_profile: User = profile.user
        user = User.objects.get(pk=user_profile.id)
    except User.DoesNotExist or Profile.DoesNotExist:
        user = None
    return user
