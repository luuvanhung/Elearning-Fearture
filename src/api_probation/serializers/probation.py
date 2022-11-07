from api_probation.models import Probation, ProbationCompetence, ProbationOverallComment, ProbationReminder
from api_probation.serializers.probation_competence import ListProbationCompetenceSerializer
from api_probation.serializers.probation_overall_comment import ListProbationOverallCommentSerializer
from api_team.serializers import TeamSerializers
from api_user.models import Profile
from api_user.serializers import TitleSerializer, UserSerializer
from django.db.models import Q
from rest_framework import serializers


class ListProbationSerializer(serializers.ModelSerializer):
    employee = UserSerializer(many=False, read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.probation_end_date:
            reminder_dates = ProbationReminder.objects.filter(
                probation_id=instance.id, reminder_status=0
            ).values_list("reminder_date", flat=True)
            if not len(reminder_dates):
                ret["remind"] = "No reminder"
            else:
                ret["remind"] = reminder_dates

        type_name = ""
        evaluation_template_name = ""
        evaluation_template_obj = (
            Probation.objects.filter(pk=instance.id).first().evaluation_template
        )
        if evaluation_template_obj:
            evaluation_template_name = evaluation_template_obj.name
            type_obj = evaluation_template_obj.type
            if type_obj:
                type_name = type_obj.type_name
        ret["type_name"] = type_name
        ret["evaluation_template_name"] = evaluation_template_name

        return ret

    class Meta:
        model = Probation
        fields = "__all__"


class ProbationSerializer(serializers.ModelSerializer):
    employee = UserSerializer(many=False, read_only=True)
    title = TitleSerializer(many=True, read_only=True)
    team = TeamSerializers(many=False, read_only=True)
    competencies = ListProbationCompetenceSerializer(many=True, read_only=True)
    overall_comments = ListProbationOverallCommentSerializer(many=True, read_only=True)
    probation_line_manager = UserSerializer(many=False, read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        self_title = "Self-evaluation"
        number_of_self_competence = ProbationCompetence.objects.filter(
            Q(probation_id=instance.id),
            Q(evaluation_template_competence_assessor_role__assessor_role=self_title),
            ~Q(score__exact=0) | ~Q(comments__exact=""),
        ).count()
        number_of_self_overall = ProbationOverallComment.objects.filter(
            Q(probation_id=instance.id),
            Q(
                evaluation_template_overall_comment_assessor_role__overall_comment_role=self_title
            ),
            ~Q(score__exact=0) | ~Q(comments__exact=""),
        ).count()

        if number_of_self_competence == 0 and number_of_self_overall == 0:
            ret["is_self_evaluated"] = False
        else:
            ret["is_self_evaluated"] = True
        return ret

    def update(self, instance, validated_data):
        from api_probation.services.probation_reminder import ProbationReminderService

        probation_id = instance.get("id", "")
        probation = Probation.objects.filter(id=probation_id).update(
            probation_end_date=instance.get("probation_end_date"),
            self_evaluation_end_date=instance.get("self_evaluation_end_date"),
            signing_official_labor_contract=instance.get(
                "signing_official_labor_contract"
            ),
            labor_contract_term=instance.get("labor_contract_term"),
            other_actions_and_updates=instance.get("other_actions_and_updates"),
            probation_line_manager=instance.get("probation_line_manager"),
            approved=instance.get("approved"),
        )

        ProbationReminderService.update_reminder_date(probation_id, instance)
        return probation

    class Meta:
        model = Probation
        fields = "__all__"
        include = ["competencies", "overall_comments"]
        depth = 1


class CreateProbationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probation
        fields = "__all__"


class ProbationReminderUserSerializer(serializers.ModelSerializer):
    employee = UserSerializer(many=False, read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        competence_assessor_ids = (
            ProbationCompetence.objects.filter(probation_id=instance.id)
            .order_by("assessor_id")
            .values_list("assessor_id", flat=True)
            .distinct()
        )
        overall_assessor_ids = (
            ProbationOverallComment.objects.filter(probation_id=instance.id)
            .order_by("assessor_id")
            .values_list("assessor_id", flat=True)
            .distinct()
        )
        reminder_user = (
            Profile.objects.filter(
                Q(user_id__in=overall_assessor_ids)
                | Q(user_id__in=competence_assessor_ids)
                | Q(user_id=instance.employee.id)
                | Q(user_id=instance.probation_line_manager)
            )
            .exclude(user_id=instance.employee.id)
            .values("slack_id", "name", "personal_email")
        )
        ret["reminder_user"] = reminder_user if reminder_user.exists() else []

        return ret

    class Meta:
        model = Probation
        fields = "__all__"
