from api_base.views import BaseViewSet
from api_user.models import Photo
from api_user.permissions import IsOwnerOrHasScope
from api_user.serializers import PhotoSerializer
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response


class PhotoViewSet(BaseViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = [OrderingFilter]
    pagination_class = None
    ordering_fields = ["created_at"]
    permission_classes = [IsOwnerOrHasScope]
    required_alternate_scopes = {
        "create": [["user:edit_public_user_information_list"], ["user:access_personal"]],
        "retrieve": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "update": [["user:edit_public_user_information_list"], ["user:access_personal"]],
        "destroy": [["user:edit_public_user_information_list"], ["user:access_personal"]],
        "list": [["user:view_public_user_information_list"], ["user:access_personal"]],
    }

    def create(self, request, *args, **kwargs):
        rs = []
        # TODO Check UI for this
        data = request.data.copy()
        for image in data.getlist("image"):
            data["photo"] = image
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            rs.append(serializer.data)
        return Response(rs, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(
            profile=kwargs.get("pk")
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
