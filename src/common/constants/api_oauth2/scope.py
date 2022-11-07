from common.constants.base_const import Const

__all__ = ["Scope"]


class Scope(Const):
    GROUP_SCOPE = {
        "user": "User",
        "admin": "User",
        "profile": "User",
        "title": "Title",
        "user_bank": "User",
        "user_lunch": "Lunch",
        "group": "Office",
        "holiday": "Office",
        "office": "Office",
        "leaves": "Leave",
        "remain_leave": "Leave",
        "request_action": "Leave",
        "request_off": "Leave",
        "bonus_leave": "Leave",
        "statistic_dateoff": "Leave",
        "dates": "Leave",
        "type_off": "Leave",
        "type_pay": "Leave",
        "lunches": "Lunch",
        "provider": "Lunch",
        "role": "Role",
        "skill": "Skill",
        "skill_definition": "Skill",
        "skill_level": "Skill",
        "skill_report": "Skill",
        "title_skill": "Skill",
        "personal_skill": "Skill",
        "team": "Team",
        "application": "Application",
        "evaluation_template": "Evaluation Template",
        "probation": "Probation",
        "elearning_topic": "E-Learning (Topic)",
        "elearning_course": "E-Learning (Course)",
        "elearning_assignment": "E-Learning (Assignment)",
    }
