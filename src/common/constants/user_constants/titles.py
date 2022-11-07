from common.constants.base_const import Const

__all__ = ["TitleConstant"]


class TitleConstant(Const):
    DIRECTOR = "Director"
    SOFTWARE_ARCHITECT = "Software architect"
    PROJECT_MANAGER = "Project manager"
    HEAD_OF_HR_AND_COMMUNICATION = "Head of HR & Communication"
    HR_EXECUTIVE = "HR Executive"
    ACCOUNTANT = "Accountant"
    TEAM_LEADER = "Team leader"
    SUB_TEAM_LEADER = "Sub-team leader"
    DEVELOPER = "Developer"
    MANUAL_TESTER = "Manual Tester"
    AUTOMATION_TESTER = "Automation Tester"

    @classmethod
    def get_title_list(cls):
        return [
            cls.DIRECTOR,
            cls.SOFTWARE_ARCHITECT,
            cls.PROJECT_MANAGER,
            cls.HEAD_OF_HR_AND_COMMUNICATION,
            cls.HR_EXECUTIVE,
            cls.ACCOUNTANT,
            cls.TEAM_LEADER,
            cls.SUB_TEAM_LEADER,
            cls.DEVELOPER,
            cls.MANUAL_TESTER,
            cls.AUTOMATION_TESTER,
        ]
