from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_base.views import ElearningBaseViewSet
from api_elearning.models import Assignment
from api_elearning.serializers import AssignmentSerializer, CourseSerializer
from api_elearning.serializers.assignment import AssignmentReadSerializer
from api_elearning.services import AssignmentService
from common.constants.api_constants import HttpMethod


class AssignmentViewSet(ElearningBaseViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    serializer_map = {
        "list": AssignmentReadSerializer,
    }
    required_alternate_scopes = {
        "PUT": [["elearning_assignment:edit"]],
        "POST": [["elearning_assignment:edit"]],
        "DELETE": [["elearning_assignment:edit"]],
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        assignments = [({**data, 'user_id': assignment}) for assignment in
                       data.get('user_ids')]
        serializer = self.serializer_class(data=assignments, many=True, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                course_instance = CourseSerializer(validated_data[0]['course']).data
                instances = AssignmentService.create_assignment(validated_data, course_instance)
                response = {'assignments': AssignmentReadSerializer(instances, many=True).data,
                            'message': 'Assignment added!'}
                return Response(response, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = AssignmentReadSerializer(instance).data
                response['message'] = 'Assignment updated!'
                return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        params = request.query_params
        try:
            assignment_queryset = AssignmentService.get_all_assignments(params).order_by('-created_at')
            page = self.paginate_queryset(assignment_queryset)
            res_data = AssignmentReadSerializer(
                page, many=True, context=self.get_parser_context(request)).data
            return self.get_paginated_response(res_data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_my_assignments(self, request, *args, **kwargs):
        user_id = request.user.id
        params = request.query_params
        try:
            assignment_queryset = AssignmentService.get_my_assignments(user_id, params)
            page = self.paginate_queryset(assignment_queryset)
            data = CourseSerializer(page, many=True, context=self.get_parser_context(request)).data
            return self.get_paginated_response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.POST], detail=False)
    def get_or_create_assignment(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user_id'] = request.user.id
        serializer = self.serializer_class(data=data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                course_instance = CourseSerializer(validated_data['course']).data
                instances = AssignmentService.get_or_create_assignment(validated_data, course_instance)
                return Response(AssignmentReadSerializer(instances).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
