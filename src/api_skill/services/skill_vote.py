from api_base.services import BaseService
from api_skill.models import SkillVote
from common.utils import Utils
from django.db import connection
from django.db.models import F


class SkillVoteService(BaseService):
    SELECT_ALL_QUERY = """
        SELECT
            `sv`.id as id,
            `profile`.name as voted_user_name,
            `sv`.voted_user_id as voted_user_id,
            `sd`.id as definition_id
        FROM hr_skill_votes `sv`
        INNER JOIN hr_skill_definitions `sd`
            ON sv.skill_definition_id = sd.id
        INNER JOIN hr_skill_levels `sl`
            ON sd.level_id = sl.id
        INNER JOIN hr_users `voter_user`
            ON sv.voter_id = voter_user.id
        INNER JOIN hr_users `voted_user`
            ON sv.voted_user_id = voted_user.id
        INNER JOIN hr_profiles `profile`
            ON sv.voted_user_id = `profile`.user_id
        LEFT OUTER JOIN hr_users_title `user_title`
            ON voter_user.id = user_title.user_id
        LEFT OUTER JOIN hr_titles `title`
            ON user_title.titles_id = title.id
        {where_condition}
        ORDER BY sv.voted_user_id ASC"""

    SEARCH_SKILL_QUERY = """
        SELECT GROUP_CONCAT(`all_records`.id SEPARATOR ',') as ids
        FROM
            (
                SELECT
                    `sv`.id as id,
                    `profile`.name as voted_user_name,
                    `sv`.voted_user_id as voted_user_id,
                    `sd`.id as definition_id
                FROM hr_skill_votes `sv`
                INNER JOIN hr_skill_definitions `sd`
                    ON sv.skill_definition_id = sd.id
                INNER JOIN hr_skill_levels `sl`
                    ON sd.level_id = sl.id
                INNER JOIN hr_users `voter_user`
                    ON sv.voter_id = voter_user.id
                INNER JOIN hr_users `voted_user`
                    ON sv.voted_user_id = voted_user.id
                INNER JOIN hr_profiles `profile`
                    ON sv.voted_user_id = `profile`.user_id
                LEFT OUTER JOIN hr_users_title `user_title`
                    ON voter_user.id = user_title.user_id
                LEFT OUTER JOIN hr_titles `title`
                    ON user_title.titles_id = title.id
                ORDER BY sv.voted_user_id ASC
            ) AS `all_records`
    """

    VOTED_USER_ID_QUERY = """
        WHERE `sv`.voted_user_id = %(voted_user_id)s
    """

    VOTED_USER_NAME_QUERY = """
            LOWER(`all_records`.voted_user_name) LIKE LOWER(%(voted_user_name)s)
    """

    DEFINITION_CONDITION_WHERE_SEARCH_QUERY = """
            `all_records`.definition_id IN %(skill_definitions)s
    """

    GROUP_BY_QUERY = """
            GROUP BY `all_records`.voted_user_id
    """

    DEFINITION_CONDITION_INTERSECT_QUERY = """
            HAVING COUNT(DISTINCT `all_records`.definition_id) = %(skill_definition_length)s
    """

    LIMIT_QUERY = """
        LIMIT %(offset)s, %(limit)s
    """

    @classmethod
    def count_level_skill(cls):
        sql_raw_query = cls.SELECT_ALL_QUERY.format(where_condition="")
        data = SkillVote.objects.raw(sql_raw_query)
        return data

    @classmethod
    def get_all(cls, request_params):
        query_params = cls.get_params(request_params)
        pagination_query_data = cls.get_pagination_query_data(request_params)
        query_params.update(pagination_query_data)

        raw_query = cls.create_raw_query_search(query_params, pagination_query_data)
        cursor = connection.cursor()
        cursor.execute(raw_query, query_params)
        row = cursor.fetchall()
        if not row:
            return 0, None
        ids_string = ""
        for el in row:
            ids_string += el[0] + ","
        ids_string = ids_string[:-1]
        ids = [int(str_id) for str_id in ids_string.split(",")]
        pagination_ids = cls.get_pagination_ids(ids, pagination_query_data)
        return len(ids), SkillVote.objects.filter(id__in=pagination_ids)

    @classmethod
    def get_current_skills(cls, user_id):
        user_id = user_id.replace("-", "")
        query_set = (
            SkillVote.objects.filter(voted_user=user_id)
            .values(
                "id",
                "voter",
                "skill_definition",
                voter_name=F("voter__profile__name"),
                skill_id=F("skill_definition__skill"),
                skill_name=F("skill_definition__skill__name"),
                level_id=F("skill_definition__level"),
                level_name=F("skill_definition__level__name"),
            )
            .order_by("skill_definition__skill__name")
        )
        return query_set

    @classmethod
    def get_pagination_ids(cls, ids, pagination_query_data):
        start_index = pagination_query_data["offset"]
        end_index = start_index + pagination_query_data["limit"]
        if start_index >= len(ids):
            return None
        if end_index > len(ids):
            return ids[start_index:]
        return ids[start_index:end_index]

    @classmethod
    def create_raw_query_search(cls, query_params, pagination_query_data):
        voted_user_name = query_params.get("voted_user_name", "")
        skill_definitions = query_params.get("skill_definitions", ())
        logic_union = query_params.get("logic_union")

        raw_query = cls.SEARCH_SKILL_QUERY

        if voted_user_name == "%%" and not skill_definitions:
            return raw_query + cls.GROUP_BY_QUERY

        raw_query += "\tWHERE "
        if voted_user_name:
            raw_query += cls.VOTED_USER_NAME_QUERY
        if skill_definitions:
            if voted_user_name:
                raw_query += "\t\t\tAND "
            raw_query += cls.DEFINITION_CONDITION_WHERE_SEARCH_QUERY

        raw_query += cls.GROUP_BY_QUERY

        if logic_union:
            return raw_query
        return raw_query + cls.DEFINITION_CONDITION_INTERSECT_QUERY

    @classmethod
    def get_params(cls, request_params):
        voted_user_name = request_params.get("q", "")
        skill_definitions = request_params.getlist("skill-definitions", [])
        intersect_condition = request_params.get("i", "0")
        logic_union = True if intersect_condition == "0" else False
        skill_definitions = tuple(int(str_id) for str_id in skill_definitions)
        skill_definition_length = len(skill_definitions)

        return {
            "voted_user_name": ("%" + voted_user_name.lower() + "%"),
            "skill_definitions": skill_definitions,
            "skill_definition_length": skill_definition_length,
            "logic_union": logic_union,
        }

    @classmethod
    def get_pagination_query_data(cls, request_params):
        page_number = Utils.cast_to_int(request_params.get("page", None), 1)
        page_size = Utils.cast_to_int(request_params.get("page-size", None), 12)

        limit = page_size
        offset = (page_number - 1) * page_size
        return {"limit": limit, "offset": offset}

    @classmethod
    def is_valid_vote(cls, validated_data, exclude_id=None):
        voter = validated_data.get("voter")
        voted_user = validated_data.get("voted_user")
        skill_definition = validated_data.get("skill_definition")
        error_message = ""

        if validated_data.get("voter") == validated_data.get("voted_user"):
            error_message = "You cannot vote yourself"

        skill_vote = SkillVote.objects.filter(
            voter=voter,
            voted_user=voted_user,
            skill_definition__skill=skill_definition.skill,
        ).exclude(id=exclude_id)
        if skill_vote.exists():
            error_message = "Voter, voted user and skill is unique"
        return error_message

    @classmethod
    def delete_record(cls, access_user, record_id):
        skill_vote = SkillVote.objects.filter(id=record_id).first()
        if skill_vote:
            if skill_vote.voter != access_user:
                return False
            else:
                skill_vote.delete()
                return True
        return False
