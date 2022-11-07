from api_base.services import BaseService, SendMail, TokenUtil
from api_user.services import UserService
from common.constants.api_constants import StaticUrls
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError


class LoginService(BaseService):
    """
    LOGIN METHOD
    """

    @classmethod
    def login(cls, **kwargs):
        try:
            email = kwargs.get("email")
            password = kwargs.get("password")
            user = UserService.get_user_by_email(email)
            if not user or not user.check_password(password):
                raise ValidationError("Invalid username or password")
            token = TokenUtil.encode(user)

            res = dict(
                success=True,
                token=token,
                user=user.id,
                profile_id=user.profile.id,
                name=user.profile.name,
                email=user.email,
                active=user.active,
                admin=user.is_admin,
                image=user.profile.image,
            )

            if user.profile.image:
                res.update(image=user.profile.image.url)
            else:
                res.update(image=None)
            return res
        except Exception as e:
            raise e

    @classmethod
    def forgot_password(cls, email, base_link="{settings.UI_HOST}/resetPassword"):
        user = UserService.get_user_by_email(email)
        if user:
            token = TokenUtil.encode(user)
            link = f"{base_link}?token={token}"
            # TODO: Get link image from CDN
            logo_img_link = StaticUrls.LOGO_IMAGE
            content = render_to_string(
                "../templates/password_email.html",
                {"link": link, "logo": logo_img_link},
            )
            SendMail.start([email], "Forgot Password", content)
            return True
        return False

    @classmethod
    def change_password(cls, user, password):
        user.set_password(password)
        user.save()
