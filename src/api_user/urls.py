from rest_framework import routers

from .views import *

app_name = "api_user"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"photo", PhotoViewSet, basename="photo")
router.register(r"bank", UserBankViewSet, basename="user_bank")
router.register(r"title", TitleViewSet, basename="title")
router.register(r"bank_list", BankViewSet, basename="banks")
router.register(r"contact", UserContactViewSet, basename="contact")
router.register(r"education", UserEducationViewSet, basename="education")
router.register(r"family", UserFamilyMembersViewSet, basename="family")
router.register(r"identity", UserIdentityViewSet, basename="identity")
router.register(r"insurance", UserInsuranceViewSet, basename="insurance")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"role", RoleViewSet, basename="role")
router.register(r"", UserViewSet, basename="user")

urlpatterns = router.urls
