from api_base.views import ElearningBaseViewSet
from api_elearning.models import Course
from api_elearning.serializers import CourseSerializer
from api_elearning.serializers.course import CourseListSerializer
from api_elearning.services import CourseService
from api_user.serializers import UserVoteSerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response


class CourseViewSet(ElearningBaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = (MultiPartParser, FormParser)
    required_alternate_scopes = {
        "create": [["elearning_course:create"]],
        "retrieve": [["elearning_course:view_list_library"]],
        "update": [["elearning_course:edit"]],
        "destroy": [["elearning_course:destroy"]],
        "list": [["elearning_course:view_list_library"]],
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        topic_ids = data.get('topic_ids')
        if topic_ids is not None and len(topic_ids) == 0:
            data['topic_ids'] = None
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = serializer.data
                response['message'] = 'Course created!'
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        topic_ids = data.get('topic_ids')
        if topic_ids is not None and len(topic_ids) == 0:
            data['topic_ids'] = None
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = serializer.data
                response['message'] = 'Course updated!'
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        params = request.query_params
        if params.get('title'):
            queryset = queryset.filter(title__icontains=params['title'])
        if params.get('topic_ids'):
            topic_ids = params['topic_ids'].split(',')
            queryset = queryset.filter(topics__id__in=topic_ids) \
                .annotate(num_topics=Count('topics')).filter(num_topics=len(topic_ids))
        if params.get('page') and params.get('page_size'):
            page = self.paginate_queryset(queryset)
            data = CourseListSerializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            serializer = CourseListSerializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_assigned_course(self, request, *args, **kwargs):
        res_data = CourseService.get_assigned_course(request.user.id, params=request.query_params)
        page = self.paginate_queryset(res_data)
        data = CourseListSerializer(page, many=True).data
        return self.get_paginated_response(data)

    @action(detail=True, methods=['get'])
    def get_exclude_users_assignment(self, request, *args, **kwargs):
        instance = self.get_object()
        exclude_users = CourseService.get_exclude_users_assignment(instance.id)
        return Response(UserVoteSerializer(exclude_users, many=True).data, status=status.HTTP_200_OK)
