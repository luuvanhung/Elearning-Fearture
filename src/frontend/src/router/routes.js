// Login
import login from "@/pages/login/index.vue";
import id_change_password from "@/pages/changepassword/index.vue";
import id_verify from "@/pages/verify/index.vue";

// After Login
import loggedInLayout from "@/layouts/loggedInLayout.vue";
import companyCalendar from "@/pages/companyCalendar/index.vue";

// Skill
import Skill from "@/pages/skill/index";
import SearchSkill from "@/pages/skill/Search/index";
import ReportSkill from "@/pages/skill/Reports/index";
import LevelSkill from "@/pages/skill/Level/Levels";
import DefinitionSkill from "@/pages/skill/Definition";
import PositionSkill from "@/pages/skill/PositionSkill";

// Team
import CreateTeam from "@/pages/createteam/index.vue";
import id_team_table from "@/pages/team/_id/index.vue";
import team_table from "@/pages/team/index.vue";
import id_edit_team from "@/pages/addMember/_id/index.vue";
import ImportFileExcel from "@/pages/team/components/ImportFileExcel";

// Lunch Management
import LunchCalendar from "@/pages/lunchCalendar/index";
import ManageLunch from "@/pages/lunchSchedule/manage.vue";
import ManageProvider from "@/pages/lunchProvider/manage.vue";
import AutoBooking from "@/pages/lunchAutoBooking/autobooking.vue";

// Role
import ManageRole from "@/pages/role/index.vue";

// Evaluation Template
import listProbation from "@/pages/evaluationTemplate/listProbation/listProbation";
import EvaluationTemplateManage from "@/pages/evaluationTemplate/evaluationTemplateManage";
import MyEvaluationTemplate from "@/pages/evaluationTemplate/myEvaluationTemplate/myEvaluationTemplate";
import AddNewEvaluationTemplate from "@/pages/evaluationTemplate/myEvaluationTemplate/addNewEvaluationTemplate";
import id_evaluation_template from "@/pages/evaluationTemplate/myEvaluationTemplate/editEvaluationTemplate";
import EvaluationTemplateFormType from "@/pages/evaluationTemplate/myEvaluationTemplate/evaluationTemplateType";

// Title
import titles from "@/pages/titles/index.vue";

// Leave
import LeaveReport from "@/pages/leaveReport/leaveReport";
import MyReport from "@/pages/leaveReport/myReport/index";
import TeamReport from "@/pages/leaveReport/teamReport/index";
import OfficeReport from "@/pages/leaveReport/officeReport/index";
import LeaveManage from "@/pages/leaveManage/leaveManage";
import MyRequest from "@/pages/leaveManage/myRequest/myRequest";
import AddNewRequest from "@/pages/leaveManage/myRequest/addNewRequest";
import Approval from "@/pages/leaveManage/approval/approval";
import OfficeRequest from "@/pages/leaveManage/officeRequest/officeRequest";
import LeaveTypesMain from "@/pages/leaveTypeOff/index";
import LeaveType from "@/pages/leaveTypeOff/LeaveType";
import LeaveTypeGroup from "@/pages/leaveTypeOff/LeaveTypeGroup";
import BonusLeave from "@/pages/leaveBonus/BonusLeave";
import BonusTypes from "@/pages/leaveBonus/bonusTypes";
import BonusLeavesMain from "@/pages/leaveBonus";

//Probation
import ProbationDetail from "@/pages/probationDetail/index.vue";
import NewProbation from "@/pages/probationDetail/addNewProbation.vue";
import ImportExcelProbation from "../pages/probationDetail/importExcel/importExcelProbation";
// User + Profile
import profile from "../pages/profile/_id/index.vue";
import id_list_table from "@/pages/employeelist/index.vue";
import ResetPassword from "@/pages/resetPassword/index.vue";

// Office
import office from "@/pages/office/index.vue";
import officeDetail from "@/pages/office/detail/index.vue";
import OrganizationChart from "@/pages/organizationChart/index.vue";

// Seat map
import SeatMap from "@/pages/seatMap/index.vue";

// Application
import IntegratedApplication from "@/pages/application/index";

// default
import Page404 from "@/pages/page404/index.vue";

//Work From Home
import WFHManage from "@/pages/wfhManage/wfhManage";
import WFHRequest from "@/pages/wfhManage/wfhRequest/wfhRequest";
import AddNewWFHRequest from "@/pages/wfhManage/wfhRequest/addNewWFHRequest";
import WFHOfficeRequest from "@/pages/wfhManage/wfhofficeRequest/wfhOfficeRequest";
import { ROUTERS } from "@/const/router";

// E-learning
import Courses from "@/pages/elearningCourses";
import courseRouter from "@/pages/elearningCourses/routerPages/course.vue";
import CourseCreate from "@/pages/elearningCourses/create/index.vue";
import CourseDetail from "@/pages/elearningCourses/detail/index.vue";
import CourseEdit from "@/pages/elearningCourses/edit/index.vue";
import CourseStudy from "@/pages/elearningCourses/study/index.vue";
import Topics from "@/pages/elearningTopics";
import QuizDetail from "@/pages/elearningCourses/Quizzes";
import MyAssignments from "@/pages/courseManagement/MyAssignments";
import assignments from "@/pages/assignments";

export const routes = [
  {
    path: ROUTERS["Login"],
    name: "Login",
    meta: {
      title: "Title",
    },
    component: login,
  },
  {
    path: ROUTERS["ResetPassword"],
    name: "ResetPassword",
    meta: {
      title: "Reset Password",
    },
    component: ResetPassword,
  },
  {
    path: ROUTERS["LoggedInLayout"],
    component: loggedInLayout,
    children: [
      {
        path: ROUTERS["Calendar"],
        name: "Calendar",
        meta: {
          title: "Company Calendar",
        },
        component: companyCalendar,
      },
      {
        path: ROUTERS["Profile"],
        name: "profile",
        component: profile,
        meta: {
          title: "Personal Information",
        },
      },
      {
        path: ROUTERS["CreateTeam"],
        name: "CreateTeam",
        meta: {
          title: "Create New Team",
        },
        component: CreateTeam,
      },
      {
        path: ROUTERS["ImportFromExcel"],
        name: "ImportFileExcel",
        component: ImportFileExcel,
        meta: {
          title: "Import File Excel",
        },
      },
      {
        path: ROUTERS["AddMember"],
        name: "AddMember",
        meta: {
          title: "Add New Member",
        },
        component: id_edit_team,
      },
      {
        path: ROUTERS["EmployeeList"],
        name: "EmployeeList",
        meta: {
          title: "Employee Accounts",
        },
        component: id_list_table,
      },
      {
        path: ROUTERS["Evaluations"],
        name: "Evaluations",
        meta: {
          title: "Evaluations",
        },
        component: listProbation,
      },
      {
        path: ROUTERS["NewEvaluation"],
        name: "New Evaluation",
        meta: {
          title: "New Evaluation",
        },
        component: NewProbation,
      },
      {
        path: ROUTERS["EvaluationImportExcel"],
        name: "Import Excel",
        meta: {
          title: "Import Excel",
        },
        component: ImportExcelProbation,
      },
      {
        path: ROUTERS["EvaluationDetail"],
        name: "Evaluation Detail",
        meta: {
          title: "Evaluation Detail",
        },
        component: ProbationDetail,
      },
      {
        path: ROUTERS["LeaveReports"],
        name: "LeaveReport",
        component: LeaveReport,
        children: [
          {
            path: ROUTERS["MyReport"],
            name: "MyReport",
            meta: {
              title: "My Report",
            },
            component: MyReport,
          },
          {
            path: ROUTERS["MyTeamReport"],
            name: "MyTeamReport",
            meta: {
              title: "Team Report",
            },
            component: TeamReport,
          },
          {
            path: ROUTERS["OfficeReport"],
            name: "OfficeReport",
            meta: {
              title: "Office Report",
            },
            component: OfficeReport,
          },
        ],
      },
      {
        path: ROUTERS["BonusLeaves"],
        name: "BonusLeaves",
        component: BonusLeavesMain,
        children: [
          {
            path: ROUTERS["BonusLeave"],
            name: "BonusLeaves",
            meta: {
              title: "Bonus Leave",
            },
            component: BonusLeave,
          },
          {
            path: ROUTERS["BonusType"],
            name: "BonusType",
            meta: {
              title: "Bonus Type",
            },
            component: BonusTypes,
          },
        ],
      },
      {
        path: ROUTERS["EvaluationTemplateManage"],
        name: "EvaluationTemplateManage",
        component: EvaluationTemplateManage,
        children: [
          {
            path: ROUTERS["MyEvaluationTemplate"],
            name: "MyEvaluationTemplate",
            meta: {
              title: "Evaluation Form Template",
            },
            component: MyEvaluationTemplate,
          },
          {
            path: ROUTERS["EvaluationTemplateFormType"],
            name: "EvaluationTemplateFormType",
            meta: {
              title: "Evaluation Template Form Type",
            },
            component: EvaluationTemplateFormType,
          },
          {
            path: ROUTERS["AddNewEvaluationTemplate"],
            name: "AddNewEvaluationTemplate",
            meta: {
              title: "Add New Evaluation Template",
            },
            component: AddNewEvaluationTemplate,
          },
          {
            path: ROUTERS["EditEvaluationTemplate"],
            name: "EditEvaluationTemplate",
            meta: {
              title: "Edit Evaluation Template",
            },
            component: id_evaluation_template,
          },
        ],
      },
      {
        path: ROUTERS["LeaveManage"],
        name: "LeaveManage",
        component: LeaveManage,
        children: [
          {
            path: ROUTERS["MyRequest"],
            name: "MyRequest",
            meta: {
              title: "My Request",
            },
            component: MyRequest,
          },
          {
            path: ROUTERS["AddNewRequest"],
            name: "AddNewRequest",
            meta: {
              title: "Add New Request",
            },
            component: AddNewRequest,
          },
          {
            path: ROUTERS["RequestApproval"],
            name: "RequestApproval",
            meta: {
              title: "Approval",
            },
            component: Approval,
          },
          {
            path: ROUTERS["OfficeRequest"],
            name: "OfficeRequest",
            meta: {
              title: "Office Request",
            },
            component: OfficeRequest,
          },
        ],
      },
      {
        path: ROUTERS["WFHManage"],
        name: "WFHManage",
        component: WFHManage,
        children: [
          {
            path: ROUTERS["WFHRequest"],
            name: "WFHRequest",
            meta: {
              title: "WFH Request",
            },
            component: WFHRequest,
          },
          {
            path: ROUTERS["AddNewRequest"],
            name: "AddNewWFHRequest1",
            meta: {
              title: "Add New WFH Request",
            },
            component: AddNewWFHRequest,
          },
          {
            path: ROUTERS["WFHOfficeRequest"],
            name: "WFHOfficeRequest",
            meta: {
              title: "WFH Office Request",
            },
            component: WFHOfficeRequest,
          },
        ],
      },
      {
        path: ROUTERS["ChangePassword"],
        name: "ChangePassword",
        meta: {
          title: "Change Password",
        },
        component: id_change_password,
      },
      {
        path: ROUTERS["TeamDetail"],
        name: "Team-id",
        meta: {
          title: "Team Profile",
        },
        component: id_team_table,
      },
      {
        path: ROUTERS["Teams"],
        name: "Team",
        meta: {
          title: "Team",
        },
        component: team_table,
      },
      {
        path: ROUTERS["Verify"],
        name: "Verify",
        meta: {
          title: "Verify",
        },
        component: id_verify,
      },
      {
        path: ROUTERS["LunchProviders"],
        name: "lunch-providers",
        meta: {
          title: "Manage Provider",
        },
        component: ManageProvider,
      },
      {
        path: ROUTERS["LunchBookings"],
        name: "lunch-bookings",
        meta: {
          title: "Auto Booking Lunch",
        },
        component: AutoBooking,
      },
      {
        path: ROUTERS["LunchSchedules"],
        name: "lunch-schedules",
        meta: {
          title: "Schedule",
        },
        component: ManageLunch,
      },
      {
        path: ROUTERS["LeaveTypes"],
        component: LeaveTypesMain,
        children: [
          {
            path: ROUTERS["LeaveTypesChild"],
            name: "leave-types",
            meta: {
              title: "Leave Types",
            },
            component: LeaveType,
          },
          {
            path: ROUTERS["LeaveTypeGroups"],
            name: "leave-type-groups",
            meta: {
              title: "Group Leave Types",
            },
            component: LeaveTypeGroup,
          },
        ],
      },
      {
        path: ROUTERS["LunchCalendar"],
        name: "LunchCalendar",
        meta: {
          title: "Meals",
        },
        component: LunchCalendar,
      },
      {
        path: ROUTERS["OrganizationChart"],
        name: "OrganizationChart",
        component: OrganizationChart,
        meta: {
          title: "Organization Chart",
        },
      },
      {
        path: ROUTERS["Skill"],
        name: "Skill",
        component: Skill,
        children: [
          {
            path: ROUTERS["SearchSkill"],
            name: "Search",
            meta: {
              title: "Search",
            },
            component: SearchSkill,
          },
          {
            path: ROUTERS["ReportSkill"],
            name: "Reports",
            meta: {
              title: "Reports",
            },
            component: ReportSkill,
          },
          {
            path: ROUTERS["LevelSkill"],
            name: "Levels",
            meta: {
              title: "Levels",
            },
            component: LevelSkill,
          },
          {
            path: ROUTERS["DefinitionSkill"],
            name: "Definitions",
            meta: {
              title: "Definitions",
            },
            component: DefinitionSkill,
          },
          {
            path: ROUTERS["PositionSkill"],
            name: "Position",
            meta: {
              title: "Position",
            },
            component: PositionSkill,
          },
        ],
      },
      {
        path: ROUTERS["Titles"],
        name: "Titles",
        meta: {
          title: "Titles",
        },
        component: titles,
      },
      {
        path: ROUTERS["IntegratedApplication"],
        name: "IntegratedApplication",
        component: IntegratedApplication,
        meta: {
          title: "Integrated Application",
        },
      },
      {
        path: ROUTERS["ManageRole"],
        name: "ManageRole",
        component: ManageRole,
        meta: {
          title: "Manage Role",
        },
      },
      {
        path: ROUTERS["Office"],
        name: "Office",
        component: office,
        meta: {
          title: "Office",
        },
      },
      {
        path: ROUTERS["OfficeInformation"],
        name: "OfficeInformation",
        component: officeDetail,
        meta: {
          title: "Office Information",
        },
      },
      {
        path: ROUTERS["SeatMap"],
        name: "SeatMap",
        component: SeatMap,
        meta: {
          title: "Seat Map",
        },
      },
      {
        path: ROUTERS["Topics"],
        name: "Topics",
        meta: {
          title: "Topics",
        },
        component: Topics,
        children: [],
      },
      {
        path: ROUTERS["assignments"],
        name: "assignments",
        meta: {
          title: "Assignments",
        },
        component: assignments,
      },
      {
        path: ROUTERS["MyAssignments"],
        name: "MyAssignments",
        meta: {
          title: "My Assignments",
        },
        component: MyAssignments,
      },
      {
        path: ROUTERS["AssingnmentUser"],
        name: "Assignment",
        component: CourseStudy,
      },
      {
        path: ROUTERS["Courses"],
        name: "Courses",
        meta: {
          title: "Courses",
        },
        component: Courses,
        children: [],
      },
      {
        path: ROUTERS["CourseCreate"],
        name: "CourseCreate",
        meta: {
          title: "Add Course",
        },
        component: CourseCreate,
      },
      {
        path: ROUTERS["CourseDetail"],
        component: courseRouter,
        props: true,
        children: [
          {
            path: "edit",
            component: CourseEdit,
            name: "CourseEdit",
          },
          {
            path: "study",
            component: CourseStudy,
            name: "CourseStudy",
          },
          {
            path: ROUTERS["QuizDetail"],
            component: QuizDetail,
            name: "QuizDetail",
            props: true,
            children: [
              {
                path: "edit",
                component: QuizDetail,
                name: "EditQuizDetail",
                props: true,
              },
            ],
          },
          {
            path: "",
            name: "CourseDetail",
            component: CourseDetail,
          },
        ],
      },
      {
        path: ROUTERS["Page404"],
        name: "Page404",
        component: Page404,
      },
    ],
  },
];
