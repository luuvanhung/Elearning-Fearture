from api_base.views import ElearningBaseViewSet
from api_elearning.models import Topic
from api_elearning.serializers import TopicSerializer
from rest_framework import status
from rest_framework.response import Response


class TopicViewSet(ElearningBaseViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    required_alternate_scopes = {
        "create": [["elearning_topic:edit"]],
        "retrieve": [["elearning_topic:view"]],
        "update": [["elearning_topic:edit"]],
        "destroy": [["elearning_topic:edit"]],
        "list": [["elearning_topic:view"]],
    }

    def list(self, request, *args, **kwargs):
        queryset = Topic.objects.all()
        params = request.query_params
        if params.get('title'):
            queryset = queryset.filter(title__icontains=params['title'])
        if params.get('page') and params.get('page_size'):
            page = self.paginate_queryset(queryset)
            data = TopicSerializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = serializer.data
                response['message'] = 'Topic created!'
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Topic with this title already exists!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data)
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                response = serializer.data
                response['message'] = 'Topic updated!'
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Topic with this title already exists!"}, status=status.HTTP_400_BAD_REQUEST)
